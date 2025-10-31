import unittest
from unittest.mock import patch
from io import StringIO
import number_guessing_game as game

class TestSimple(unittest.TestCase):
    
    @patch('builtins.input', return_value='1')
    def test_difficulty(self, mock_input):
        """تست ساده انتخاب سطح"""
        attempts, difficulty = game.get_difficulty()
        self.assertEqual(attempts, 15)
        
    @patch('builtins.input', return_value='50')
    def test_guess(self, mock_input):
        """تست ساده دریافت حدس"""
        guess = game.get_guess(1, 100)
        self.assertEqual(guess, 50)

if __name__ == '__main__':
    unittest.main()