#pragma once

#include <AETK/AEGP/AEGP.hpp>
#include <atomic>
#include <thread>
#include <memory>
#include <string>

class PyShiftAE;

/**
 * Single command: opens the Python Script Editor window (Window menu)
 */
class PyScriptEditorCommand : public Command {
public:
    explicit PyScriptEditorCommand(A_long command_id);
    void execute() override;
    void updateMenu() override;
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

    void onInit()  override;
    void onDeath() override;
    void onIdle()  override;

    void ensurePythonStarted();

private:
    void startPythonThread(const std::string& pluginDir);

    std::atomic<bool> python_started{ false };
};
