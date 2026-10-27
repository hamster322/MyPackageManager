import sys
import copy
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import main

class TestAllDigits(unittest.TestCase):
    """Тесты функции all_digits"""

    def test_digits_only(self):
        self.assertTrue(main.all_digits("12345"))
        self.assertTrue(main.all_digits("0"))

    def test_not_digits(self):
        self.assertFalse(main.all_digits("12a5"))
        self.assertFalse(main.all_digits("abc"))
        self.assertFalse(main.all_digits("1.2"))
        self.assertFalse(main.all_digits(""))


class TestCheckVersion(unittest.TestCase):
    """Тесты функции check_version."""

    def test_latest(self):
        self.assertTrue(main.check_version("latest"))

    def test_valid_versions(self):
        self.assertTrue(main.check_version("1.2.3"))
        self.assertTrue(main.check_version("1.0"))

    def test_invalid_versions(self):
        self.assertFalse(main.check_version("1.a.3"))
        self.assertFalse(main.check_version("v1.2.3"))


class TestGetState(unittest.TestCase):
    """Тесты функции get_state с готовыми CSV-файлами."""

    def setUp(self):
        """Сохраняем исходное состояние"""
        self._original_state = copy.deepcopy(main.state)

    def tearDown(self):
        """Восстанавливаем state после каждого теста"""
        main.state.clear()
        main.state.update(self._original_state)

    def test_valid_config(self):
        csv_path = str(Path(__file__).parent / "valid_config.csv")
        main.get_state(csv_path)

        self.assertEqual(main.state["packageName"], "test_package")
        self.assertEqual(main.state["path"], "/tmp/test")
        self.assertEqual(main.state["mode"], "1")
        self.assertEqual(main.state["packageVersion"], "1.2.3")

    def test_invalid_version(self):
        old_version = main.state["packageVersion"]
        csv_path = str(Path(__file__).parent / "invalid_version.csv")
        main.get_state(csv_path)

        self.assertEqual(main.state["packageVersion"], old_version)

    def test_invalid_version(self):
        csv_path = str(Path(__file__).parent / "invalid_version.csv")

        with self.assertRaises(SystemExit):
            main.get_state(csv_path)

    def test_unknown_key(self):
        csv_path = str(Path(__file__).parent / "unknown_key.csv")
        main.get_state(csv_path)

        self.assertEqual(main.state["packageName"], "pkg")
        self.assertEqual(main.state["mode"], "1")


if __name__ == '__main__':
    unittest.main()