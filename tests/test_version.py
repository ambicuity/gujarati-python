import unittest
import subprocess
import sys
import os
from ગુજરાતી_પાઈથન import __version__

class TestVersionFlag(unittest.TestCase):
    """Test the --version flag functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'મુખ્ય.py')
    
    def test_version_short_flag(self):
        """Test -v flag"""
        result = subprocess.run(
            [sys.executable, self.script_path, '-v'],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(f"ગુજરાતી પાઈથન {__version__}", result.stdout.strip().splitlines()[-1])
    
    def test_version_long_flag(self):
        """Test --version flag"""
        result = subprocess.run(
            [sys.executable, self.script_path, '--version'],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(f"ગુજરાતી પાઈથન {__version__}", result.stdout.strip().splitlines()[-1])
    
    def test_version_gujarati_flag(self):
        """Test --આવૃત્તિ flag (Gujarati version flag)"""
        result = subprocess.run(
            [sys.executable, self.script_path, '--આવૃત્તિ'],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(f"ગુજરાતી પાઈથન {__version__}", result.stdout.strip().splitlines()[-1])

if __name__ == '__main__':
    unittest.main()
