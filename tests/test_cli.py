"""
Unit tests for CLI interface.
"""

import unittest
from unittest.mock import patch
import sys
from src.cli import main


class TestCLI(unittest.TestCase):
    def test_cli_help(self):
        with patch.object(sys, 'argv', ['src.cli', '--help']):
            with self.assertRaises(SystemExit) as cm:
                with patch('sys.stdout'):
                    main()
            self.assertEqual(cm.exception.code, 0)

    def test_cli_missing_prompt(self):
        with patch.object(sys, 'argv', ['src.cli']):
            with self.assertRaises(SystemExit) as cm:
                with patch('sys.stderr'):
                    main()
            self.assertNotEqual(cm.exception.code, 0)


if __name__ == '__main__':
    unittest.main()
