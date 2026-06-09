#include "PyShiftAE.h"

#include "AETK/AEGP/Core/PyFx.hpp"
#include "Python.h"

#include <pybind11/embed.h>
#include <filesystem>
#include <fstream>
#include <mutex>
#include <queue>
#include <sstream>
#include <thread>
#include <chrono>
#include <ctime>

namespace py = pybind11;
namespace fs = std::filesystem;

// ------------------------------------------------------------
// Logging
// ------------------------------------------------------------

static std::mutex log_mutex;

static fs::path getLogPath() {
    const char* appdata = std::getenv("APPDATA");
    if (!appdata) return {};
    fs::path dir = fs::path(appdata) / "PyShiftAE";
    if (!fs::exists(dir))
        fs::create_directories(dir);
    return dir / "pyshiftae.log";
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
// Globals
// ------------------------------------------------------------

AEGP_PluginID myID = 3927L;

static std::queue<std::string> script_queue;
static std::mutex script_mutex;

static std::atomic<bool> running = false;
static std::thread py_thread;

PyShiftAE* PyShiftAE::instance = nullptr;

// ------------------------------------------------------------
// Script command
// ------------------------------------------------------------

PyShiftAEScriptCommand::PyShiftAEScriptCommand(
    const std::string& label,
    A_long command_id,
    size_t script_index
)
    : Command(label.c_str(), MenuID::FILE, command_id),
    script_index(script_index) {
}

void PyShiftAEScriptCommand::execute() {
    if (!PyShiftAE::instance)
        return;

    auto& plugin = *PyShiftAE::instance;

    // ✅ Safe public call
    plugin.ensurePythonStarted();

    if (script_index >= plugin.scripts.size())
        return;

    logMessage("[execute] Queuing script index=" + std::to_string(script_index)
               + " path=" + plugin.scripts[script_index].path);

    std::lock_guard<std::mutex> lock(script_mutex);
    script_queue.push(plugin.scripts[script_index].path);
}

void PyShiftAEScriptCommand::updateMenu() {
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

std::vector<std::string> PyShiftAE::getScriptPaths() {
	const char* script_path = std::getenv("AE_SCRIPT_PATH");

    std::vector<std::string> result;

    if (!script_path || !fs::exists(script_path))
        return result;

    for (const auto& entry : fs::directory_iterator(script_path)) {
        if (entry.path().extension() == ".py") {
            result.push_back(entry.path().string());
        }
    }

    return result;
}

// ------------------------------------------------------------
// Python lifecycle (SAFE + LAZY)
// ------------------------------------------------------------

void PyShiftAE::ensurePythonStarted() {
    if (python_started.exchange(true)) {
        logMessage("[python] ensurePythonStarted: already running");
        return;
    }

    logMessage("[python] ensurePythonStarted: first call, starting thread");
    startPythonThread();
}

void PyShiftAE::startPythonThread() {
    running.store(true);

    py_thread = std::thread([]() {
        bool python_initialized = false;

        logMessage("[python] Calling Py_Initialize...");
        Py_Initialize();
        python_initialized = Py_IsInitialized();
        logMessage(std::string("[python] Py_IsInitialized = ") + (python_initialized ? "true" : "false"));

        if (python_initialized) {
            try {
                logMessage("[python] Importing PyFx...");
                py::module::import("PyFx");
                logMessage("[python] PyFx imported successfully");
            }
            catch (const std::exception& e) {
                logMessage(std::string("[python] PyFx import failed: ") + e.what());
                App::Alert("PyFx import failed");
            }
            catch (...) {
                logMessage("[python] PyFx import failed (unknown exception)");
                App::Alert("PyFx import failed");
            }
        }

        // Set up Qt integration: monkey-patch exec/exec_ so scripts
        // don't block.  Do NOT create a QApplication ourselves — the
        // scripts use FXApplication (a QApplication subclass with its
        // own singleton pattern).  The first script creates it; the
        // singleton ensures subsequent scripts reuse it.
        // processEvents() in the loop keeps every window responsive.
        try {
            logMessage("[python] Setting up Qt integration...");
            py::exec(R"(
__pyshiftae_qt_mod = None
for _mn in ('PySide6.QtWidgets', 'PySide2.QtWidgets',
            'PyQt6.QtWidgets', 'PyQt5.QtWidgets'):
    try:
        __pyshiftae_qt_mod = __import__(_mn, fromlist=['QApplication'])
        break
    except ImportError:
        continue

if __pyshiftae_qt_mod is not None:
    _QApp = __pyshiftae_qt_mod.QApplication
    _QApp.exec = lambda *a, **kw: 0
    if hasattr(_QApp, 'exec_'):
        _QApp.exec_ = lambda *a, **kw: 0

def __pyshiftae_process_qt():
    if __pyshiftae_qt_mod is None:
        return
    _inst = __pyshiftae_qt_mod.QApplication.instance()
    if _inst is not None:
        _inst.processEvents()
)");
            logMessage("[python] Qt integration ready");
        }
        catch (const std::exception& e) {
            logMessage(std::string("[python] Qt setup note: ") + e.what());
        }

        {
            // Scope block so py::object refs are destroyed before Py_Finalize
            py::object process_qt;
            try {
                process_qt = py::globals()["__pyshiftae_process_qt"];
            }
            catch (...) {
                process_qt = py::none();
            }

            while (running.load()) {
                std::string path;

                {
                    std::lock_guard<std::mutex> lock(script_mutex);
                    if (!script_queue.empty()) {
                        path = script_queue.front();
                        script_queue.pop();
                    }
                }

                if (!path.empty()) {
                    logMessage("[python] Dequeued script: " + path);
                    try {
                        logMessage("[python] Executing script: " + path);
                        py::eval_file(path.c_str());
                        logMessage("[python] Script finished: " + path);
                    }
                    catch (py::error_already_set& e) {
                        if (e.matches(PyExc_SystemExit)) {
                            logMessage("[python] Script exited via sys.exit (normal for Qt): " + path);
                        }
                        else {
                            logMessage(std::string("[python] Script error: ") + e.what());
                            App::Alert(e.what());
                        }
                    }
                    catch (const std::exception& e) {
                        logMessage(std::string("[python] Script error: ") + e.what());
                        App::Alert(e.what());
                    }
                }

                // Process Qt events to keep all open windows responsive
                if (!process_qt.is_none()) {
                    try { process_qt(); }
                    catch (...) {}
                }

                std::this_thread::sleep_for(std::chrono::milliseconds(10));
            }
        } // py::object refs released here

        logMessage("[python] Worker loop exited");

        if (python_initialized) {
            logMessage("[python] Calling Py_Finalize...");
            Py_Finalize();
            logMessage("[python] Py_Finalize done");
        }
        });
}

// ------------------------------------------------------------
// Lifecycle
// ------------------------------------------------------------

void PyShiftAE::onInit() {
    logMessage("[init] onInit called");
    auto paths = getScriptPaths();

    logMessage("[init] Found " + std::to_string(paths.size()) + " script(s)");
    for (const auto& p : paths)
        logMessage("[init]   " + p);

    // No scripts = plugin does nothing
    if (paths.empty())
        return;

    A_long base_id = 40000;

    for (size_t i = 0; i < paths.size(); ++i) {
        ScriptEntry entry;
        entry.command_id = base_id + static_cast<A_long>(i);
        entry.path = paths[i];
        entry.name = fs::path(paths[i]).stem().string();

        scripts.push_back(entry);

        addCommand(std::make_unique<PyShiftAEScriptCommand>(
            entry.name,
            entry.command_id,
            i
        ));
    }

    registerCommandHook();
    registerUpdateMenuHook();
    registerIdleHook();
}

void PyShiftAE::onDeath() {
    logMessage("[death] onDeath called");
    if (!python_started.load())
        return;

    running.store(false);
    logMessage("[death] Waiting for python thread to join...");

    if (py_thread.joinable()) {
        py_thread.join();
    }
    logMessage("[death] Python thread joined");
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
