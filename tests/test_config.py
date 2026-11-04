"""
Unit tests for configuration manager.
"""

import unittest
from src.utils.config import ConfigManager, get_config, set_config


class TestConfig(unittest.TestCase):
    def test_config_instance(self):
        cfg = ConfigManager.instance()
        self.assertIsNotNone(cfg)
        self.assertIn('auto_save', cfg.get_all())

    def test_strudel_removed_from_config(self):
        cfg = ConfigManager.instance()
        self.assertNotIn('strudel_host', cfg.get_all())

    def test_get_and_set_config(self):
        orig_val = get_config('show_tooltips', True)
        set_config('show_tooltips', False)
        self.assertFalse(get_config('show_tooltips'))
        # Restore
        set_config('show_tooltips', orig_val)


    def test_aoide_and_transcription_config_defaults(self):
        cfg = ConfigManager.instance()
        all_settings = cfg.get_all()
        self.assertIn('transcription_engine', all_settings)
        self.assertIn('muscriptor_export_velocity', all_settings)
        self.assertIn('aoide_default_route', all_settings)
        self.assertIn('aoide_comfyui_port', all_settings)
        self.assertIn('aoide_default_cot', all_settings)
        self.assertEqual(get_config('aoide_default_route'), 'package')
        self.assertEqual(get_config('aoide_comfyui_port'), 8188)


if __name__ == '__main__':
    unittest.main()
