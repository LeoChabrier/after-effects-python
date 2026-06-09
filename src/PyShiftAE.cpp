#include "PyShiftAE.h"

#include "AETK/AEGP/Core/PyFx.hpp"
#include "Python.h"

#include <pybind11/embed.h>
#include <windows.h>
#include <filesystem>
#include <fstream>
#include <mutex>
#include <queue>
#include <string>
#include <thread>
#include <chrono>
#include <ctime>
#include <atomic>

namespace py = pybind11;
namespace fs = std::filesystem;

// ------------------------------------------------------------
// Logging
// ------------------------------------------------------------

static std::mutex log_mutex;

static fs::path getLogPath() {
    const char* appdata = std::getenv("APPDATA");
    if (!appdata) return {};
    fs::path dir = fs::path(appdata) / "after-effects-python";
    if (!fs::exists(dir))
        fs::create_directories(dir);
    return dir / "plugin.log";
}

static void logMessage(const std::string& msg) {
    std::lock_guard<std::mutex> lock(log_mutex);
    fs::path logPath = getLogPath();
    if (logPath.empty()) return;
    std::ofstream ofs(logPath, std::ios::app);
    if (!ofs) return;
    auto now = std::chrono::system_clock::now();
    std::time_t t = std::chrono::system_clock::to_time_t(now);
    char buf[64];
    std::strftime(buf, sizeof(buf), "%Y-%m-%d %H:%M:%S", std::localtime(&t));
    ofs << "[" << buf << "] " << msg << "\n";
}

// ------------------------------------------------------------
// Helpers
// ------------------------------------------------------------

static std::string getDllDirectory() {
    HMODULE hModule = nullptr;
    GetModuleHandleExA(
        GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS | GET_MODULE_HANDLE_EX_FLAG_UNCHANGED_REFCOUNT,
        reinterpret_cast<LPCSTR>(&getDllDirectory),
        &hModule
    );
    char path[MAX_PATH] = {};
    GetModuleFileNameA(hModule, path, MAX_PATH);
    return fs::path(path).parent_path().string();
}

// ------------------------------------------------------------
// Globals
// ------------------------------------------------------------

AEGP_PluginID myID = 3927L;

// Code strings queued for execution in the Python thread
static std::queue<std::string> code_queue;
static std::mutex code_mutex;

static std::atomic<bool> running = false;
static std::thread py_thread;

PyShiftAE* PyShiftAE::instance = nullptr;

// ------------------------------------------------------------
// Script editor command
// ------------------------------------------------------------

PyScriptEditorCommand::PyScriptEditorCommand(A_long command_id)
    : Command("Python Script Editor", MenuID::WINDOW, command_id)
{
}

void PyScriptEditorCommand::execute() {
    if (!PyShiftAE::instance)
        return;

    PyShiftAE::instance->ensurePythonStarted();

    std::lock_guard<std::mutex> lock(code_mutex);
    code_queue.push("import PyAE.editor; PyAE.editor.main()");
}

void PyScriptEditorCommand::updateMenu() {
    SuiteManager::GetInstance()
        .GetSuiteHandler()
        .CommandSuite1()
        ->AEGP_EnableCommand(getCommand());
}

// ------------------------------------------------------------
// PyShiftAE
// ------------------------------------------------------------

PyShiftAE::PyShiftAE(
    SPBasicSuite* pica_basicP,
    AEGP_PluginID aegp_plugin_id,
    AEGP_GlobalRefcon* global_refconV
)
    : Plugin(pica_basicP, aegp_plugin_id, global_refconV) {
    instance = this;
}

void PyShiftAE::ensurePythonStarted() {
    if (python_started.exchange(true)) {
        return;
    }
    std::string pluginDir = getDllDirectory();
    logMessage("[python] Plugin dir: " + pluginDir);
    startPythonThread(pluginDir);
}

// ------------------------------------------------------------
// Python thread
// ------------------------------------------------------------

void PyShiftAE::startPythonThread(const std::string& pluginDir) {
    running.store(true);

    py_thread = std::thread([pluginDir]() {
        logMessage("[python] Py_Initialize...");
        Py_Initialize();
        bool ok = Py_IsInitialized();
        logMessage(std::string("[python] Py_IsInitialized=") + (ok ? "true" : "false"));

        if (!ok) return;

        // --- Add package search paths to sys.path ---
        // Primary: %APPDATA%\after-effects-python  (post-build copies PyAE here, no admin needed)
        // Fallback: DLL directory (useful when running from a dev layout)
        {
            std::vector<std::string> paths;

            const char* appdata = std::getenv("APPDATA");
            if (appdata) {
                paths.push_back((fs::path(appdata) / "after-effects-python").string());
            }
            if (!pluginDir.empty()) {
                paths.push_back(pluginDir);
            }

            for (const auto& p : paths) {
                try {
                    std::string escaped;
                    for (char c : p)
                        escaped += (c == '\\') ? "\\\\" : std::string(1, c);
                    py::exec("import sys\nif '" + escaped + "' not in sys.path:\n    sys.path.insert(0, '" + escaped + "')");
                    logMessage("[python] sys.path: " + p);
                }
                catch (const std::exception& e) {
                    logMessage(std::string("[python] sys.path error for ") + p + ": " + e.what());
                }
            }
        }

        // --- Import PyFx ---
        try {
            py::module::import("PyFx");
            logMessage("[python] PyFx imported");
        }
        catch (const std::exception& e) {
            logMessage(std::string("[python] PyFx import failed: ") + e.what());
            App::Alert("PyFx import failed");
        }

        // --- Qt integration: patch exec() so it doesn't block ---
        try {
            py::exec(R"(
__pyae_qt_mod = None
for _mn in ('PySide6.QtWidgets', 'PySide2.QtWidgets',
            'PyQt6.QtWidgets', 'PyQt5.QtWidgets'):
    try:
        __pyae_qt_mod = __import__(_mn, fromlist=['QApplication'])
        break
    except ImportError:
        continue

if __pyae_qt_mod is not None:
    _QApp = __pyae_qt_mod.QApplication
    _QApp.exec = lambda *a, **kw: 0
    if hasattr(_QApp, 'exec_'):
        _QApp.exec_ = lambda *a, **kw: 0

def __pyae_process_qt():
    if __pyae_qt_mod is None:
        return
    _inst = __pyae_qt_mod.QApplication.instance()
    if _inst is not None:
        _inst.processEvents()
)");
            logMessage("[python] Qt integration ready");
        }
        catch (const std::exception& e) {
            logMessage(std::string("[python] Qt setup: ") + e.what());
        }

        // --- Event loop ---
        {
            py::object process_qt;
            try {
                process_qt = py::globals()["__pyae_process_qt"];
            }
            catch (...) {
                process_qt = py::none();
            }

            while (running.load()) {
                std::string code;
                {
                    std::lock_guard<std::mutex> lock(code_mutex);
                    if (!code_queue.empty()) {
                        code = code_queue.front();
                        code_queue.pop();
                    }
                }

                if (!code.empty()) {
                    logMessage("[python] exec: " + code);
                    try {
                        py::exec(code.c_str());
                    }
                    catch (py::error_already_set& e) {
                        if (!e.matches(PyExc_SystemExit)) {
                            logMessage(std::string("[python] error: ") + e.what());
                            App::Alert(e.what());
                        }
                    }
                    catch (const std::exception& e) {
                        logMessage(std::string("[python] error: ") + e.what());
                        App::Alert(e.what());
                    }
                }

                if (!process_qt.is_none()) {
                    try { process_qt(); }
                    catch (...) {}
                }

                std::this_thread::sleep_for(std::chrono::milliseconds(10));
            }
        }

        logMessage("[python] Thread exiting, Py_Finalize...");
        Py_Finalize();
        logMessage("[python] Py_Finalize done");
    });
}

// ------------------------------------------------------------
// Lifecycle
// ------------------------------------------------------------

void PyShiftAE::onInit() {
    logMessage("[init] onInit");
    addCommand(std::make_unique<PyScriptEditorCommand>(40000));
    registerCommandHook();
    registerUpdateMenuHook();
    registerIdleHook();
}

void PyShiftAE::onDeath() {
    logMessage("[death] onDeath");
    if (!python_started.load())
        return;

    running.store(false);
    if (py_thread.joinable())
        py_thread.join();

    logMessage("[death] Thread joined");
}

void PyShiftAE::onIdle() {
    ae::TaskScheduler::GetInstance().ExecuteTask();
}

// ------------------------------------------------------------
// Entry point
// ------------------------------------------------------------

extern "C" __declspec(dllexport)
A_Err EntryPointFunc(
    SPBasicSuite* pica_basicP,
    A_long major_versionL,
    A_long minor_versionL,
    AEGP_PluginID aegp_plugin_id,
    AEGP_GlobalRefcon* global_refconV
) {
    myID = aegp_plugin_id;

    SuiteManager::GetInstance().InitializeSuiteHandler(pica_basicP);
    SuiteManager::GetInstance().SetPluginID(&myID);

    return Plugin::EntryPointFunc<PyShiftAE>(
        pica_basicP,
        major_versionL,
        minor_versionL,
        aegp_plugin_id,
        global_refconV
    );
}
