"""
Unit tests for ModelManager GPU Lease System.
"""

import unittest
from unittest.mock import MagicMock
import subprocess
import sys

from src.utils.model_manager import ModelManager


class TestModelManager(unittest.TestCase):
    def setUp(self):
        self.manager = ModelManager.instance()
        # Reset internal state
        if self.manager.current_lease:
            self.manager.release_gpu(self.manager.current_lease.owner_id)

    def test_reentrant_acquire(self):
        ok = self.manager.acquire_gpu(owner_id="model_a", kind="in_process")
        self.assertTrue(ok)
        self.assertEqual(self.manager.get_active_model_name(), "model_a")
        # Same owner re-acquires without revoking
        ok2 = self.manager.acquire_gpu(owner_id="model_a", kind="in_process")
        self.assertTrue(ok2)
        self.assertEqual(self.manager.get_active_model_name(), "model_a")

    def test_in_process_unload_on_switch(self):
        mock_loader_1 = MagicMock()
        self.manager.prepare_load(mock_loader_1, "ModelOne")
        self.assertEqual(self.manager.get_active_model_name(), "ModelOne")

        mock_loader_2 = MagicMock()
        self.manager.prepare_load(mock_loader_2, "ModelTwo")
        # Verify previous loader was unloaded
        mock_loader_1.unload.assert_called_once()
        self.assertEqual(self.manager.get_active_model_name(), "ModelTwo")

    def test_external_process_lease_revocation(self):
        # Spawn a dummy sleep process
        proc = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(10)"])
        self.assertIsNone(proc.poll())  # running

        ok = self.manager.acquire_gpu(owner_id="ext_proc_1", kind="external_process", proc=proc)
        self.assertTrue(ok)
        self.assertEqual(self.manager.get_active_model_name(), "ext_proc_1")

        # Now acquire GPU for another owner -> must terminate proc and wait for exit
        ok2 = self.manager.acquire_gpu(owner_id="in_proc_2", kind="in_process")
        self.assertTrue(ok2)
        self.assertEqual(self.manager.get_active_model_name(), "in_proc_2")
        # Confirm external process has exited
        self.assertIsNotNone(proc.poll())

    def test_release_gpu(self):
        self.manager.acquire_gpu(owner_id="test_owner", kind="in_process")
        self.assertEqual(self.manager.get_active_model_name(), "test_owner")
        self.manager.release_gpu("test_owner")
        self.assertEqual(self.manager.get_active_model_name(), "")
        self.assertIsNone(self.manager.current_lease)


if __name__ == '__main__':
    unittest.main()
