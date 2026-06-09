#pragma once

#include <AETK/AEGP/AEGP.hpp>
#include <vector>
#include <string>
#include <atomic>
#include <thread>
#include <memory>

/**
 * One Python script mapped to one AE command
 */
struct ScriptEntry {
    A_long command_id;
    std::string name;
    std::string path;
};

class PyShiftAE;

/**
 * Command executing a Python script
 */
class PyShiftAEScriptCommand : public Command {
public:
    PyShiftAEScriptCommand(
        const std::string& label,
        A_long command_id,
        size_t script_index
    );

    void execute() override;
    void updateMenu() override;

private:
    size_t script_index;
};

/**
 * Main plugin class
 */
class PyShiftAE : public Plugin {
public:
    PyShiftAE(
        struct SPBasicSuite* pica_basicP,
        AEGP_PluginID aegp_plugin_id,
        AEGP_GlobalRefcon* global_refconV
    );

    static PyShiftAE* instance;

    void onInit() override;
    void onDeath() override;
    void onIdle() override;

    static std::vector<std::string> getScriptPaths();

    // ?? PUBLIC SAFE ENTRY POINT
    void ensurePythonStarted();

    std::vector<ScriptEntry> scripts;

private:
    void startPythonThread();

    std::atomic<bool> python_started{ false };
};
