import os
os.environ["QT_QPA_PLATFORM"] = "offscreen"

import unittest
import importlib
from PyQt6.QtWidgets import QApplication

# Ensure single offscreen QApplication instance for UI widgets
_qapp = QApplication.instance() or QApplication(["test_app"])


class TestModuleImports(unittest.TestCase):
    MODULES = [
        "src.utils.config",
        "src.utils.audio",
        "src.utils.effects",
        "src.utils.performance",
        "src.utils.stems",
        "src.utils.streaming",
        "src.utils.cache",
        "src.utils.model_manager",
        "src.utils.credentials",
        "src.utils.midi",
        "src.utils.midi_muscriptor",
        "src.device",
        "src.models.transcription",
        "src.models.catalog",
        "src.models.base",
        "src.models.musicgen",
        "src.models.ace_step",
        "src.models.diffrhythm",
        "src.models.yue2",
        "src.aoide",
        "src.aoide.backend",
        "src.aoide.abc_tools",
        "src.api.server",
        "src.api.api_worker",
        "src.ui.workers",
        "src.ui.dialogs.cache_dialog",
        "src.ui.dialogs.console_window",
        "src.ui.dialogs.settings_panel",
        "src.ui.panels.arranger_panel",
        "src.ui.panels.player_panel",
        "src.ui.panels.stems_panel",
        "src.ui.panels.ace_step_panel",
        "src.ui.panels.diffrhythm_panel",
        "src.ui.panels.transcription_panel",
        "src.ui.panels.aoide_panel",
        "src.ui.main_window",
    ]

    def test_imports(self):
        for mod in self.MODULES:
            with self.subTest(module=mod):
                imported = importlib.import_module(mod)
                self.assertIsNotNone(imported)


if __name__ == '__main__':
    unittest.main()
