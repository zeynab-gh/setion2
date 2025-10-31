import unittest
from unittest.mock import patch
from io import StringIO
import random
import number_guessing_game as game

class TestNumberGuessingGame(unittest.TestCase):

    # Test welcome message display - FIXED
    def test_display_welcome(self):
        """Test that welcome message displays correctly"""
        with patch('sys.stdout', new=StringIO()) as fake_output:
            game.display_welcome()
            output = fake_output.getvalue()
            
            # فقط چیزهایی که واقعاً در display_welcome وجود دارند را چک کن
            self.assertIn("Welcome to Number Guessing Game!", output)
            self.assertIn("I'm thinking of a number between 1-100", output)
            self.assertIn("Choose difficulty and start guessing!", output)
            # "Difficulty Levels:" در display_welcome نیست، پس حذف شد

    # Test difficulty selection
    @patch('builtins.input', side_effect=['1'])
    def test_get_difficulty_easy(self, mock_input):
        """Test easy difficulty selection"""
        attempts, difficulty = game.get_difficulty()
        self.assertEqual(attempts, 15)
        self.assertEqual(difficulty, "Easy")

    @patch('builtins.input', side_effect=['2'])
    def test_get_difficulty_medium(self, mock_input):
        """Test medium difficulty selection"""
        attempts, difficulty = game.get_difficulty()
        self.assertEqual(attempts, 10)
        self.assertEqual(difficulty, "Medium")

    @patch('builtins.input', side_effect=['3'])
    def test_get_difficulty_hard(self, mock_input):
        """Test hard difficulty selection"""
        attempts, difficulty = game.get_difficulty()
        self.assertEqual(attempts, 5)
        self.assertEqual(difficulty, "Hard")

    @patch('builtins.input', side_effect=['4', '0', '2'])
    def test_get_difficulty_invalid_then_valid(self, mock_input):
        """Test invalid input then valid difficulty selection"""
        attempts, difficulty = game.get_difficulty()
        self.assertEqual(attempts, 10)
        self.assertEqual(difficulty, "Medium")

    @patch('builtins.input', side_effect=['abc', '1'])
    def test_get_difficulty_string_input_then_valid(self, mock_input):
        """Test string input then valid difficulty"""
        attempts, difficulty = game.get_difficulty()
        self.assertEqual(attempts, 15)
        self.assertEqual(difficulty, "Easy")

    # Test guess input
    @patch('builtins.input', side_effect=['50'])
    def test_get_guess_valid(self, mock_input):
        """Test valid guess input"""
        guess = game.get_guess(1, 10)
        self.assertEqual(guess, 50)

    @patch('builtins.input', side_effect=['0', '101', '75'])
    def test_get_guess_out_of_range_then_valid(self, mock_input):
        """Test out of range then valid guess"""
        guess = game.get_guess(1, 10)
        self.assertEqual(guess, 75)

    @patch('builtins.input', side_effect=['abc', '25'])
    def test_get_guess_invalid_input_then_valid(self, mock_input):
        """Test invalid input then valid guess"""
        guess = game.get_guess(1, 10)
        self.assertEqual(guess, 25)

    # Test complete game flow - Winning scenarios - FIXED
    @patch('random.randint', return_value=42)
    @patch('builtins.input', side_effect=['1', '42'])  # Easy, correct first try
    @patch('sys.stdout', new_callable=StringIO)
    def test_play_game_win_first_try(self, mock_stdout, mock_input, mock_random):
        """Test winning on first attempt"""
        game.play_game()
        output = mock_stdout.getvalue()
        
        self.assertIn("🎉 Correct! The number was 42", output)
        self.assertIn("🏆 You won in 1 attempts!", output)
        self.assertIn("Easy mode - 15 attempts", output)

    @patch('random.randint', return_value=42)
    @patch('builtins.input', side_effect=['2', '10', '20', '30', '40', '42'])  # Medium, multiple attempts
    @patch('sys.stdout', new_callable=StringIO)
    def test_play_game_win_multiple_attempts(self, mock_stdout, mock_input, mock_random):
        """Test winning after multiple attempts"""
        game.play_game()
        output = mock_stdout.getvalue()
        
        self.assertIn("🎉 Correct! The number was 42", output)
        self.assertIn("📈 Go higher!", output)

    # Test complete game flow - Losing scenario
    @patch('random.randint', return_value=42)
    @patch('builtins.input', side_effect=['3', '10', '20', '30', '40', '50'])  # Hard, all wrong guesses
    @patch('sys.stdout', new_callable=StringIO)
    def test_play_game_lose(self, mock_stdout, mock_input, mock_random):
        """Test losing the game"""
        game.play_game()
        output = mock_stdout.getvalue()
        
        self.assertIn("💔 Game Over! No attempts left.", output)
        self.assertIn("The number was: 42", output)
        self.assertIn("Hard mode - 5 attempts", output)

    # Test hint messages - FIXED
    @patch('random.randint', return_value=42)
    @patch('builtins.input', side_effect=['1', '30', '50', '42'])  # Test hints
    @patch('sys.stdout', new_callable=StringIO)
    def test_play_game_hints(self, mock_stdout, mock_input, mock_random):
        """Test hint messages (higher/lower)"""
        game.play_game()
        output = mock_stdout.getvalue()
        
        self.assertIn("📈 Go higher!", output)  # For guess 30
        self.assertIn("📉 Go lower!", output)   # For guess 50

    # Test attempts counter display - FIXED
    @patch('random.randint', return_value=42)
    @patch('builtins.input', side_effect=['1', '10', '20', '42'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_play_game_attempts_counter(self, mock_stdout, mock_input, mock_random):
        """Test attempts counter display"""
        game.play_game()
        output = mock_stdout.getvalue()
        
        # به جای جستجوی "Attempt 1/15" که در input prompt است،
        # چیزهایی که واقعاً در خروجی چاپ می‌شوند را چک کن
        self.assertIn("Attempts left: 14", output)
        self.assertIn("Attempts left: 13", output)
        self.assertIn("You won in 3 attempts!", output)

class TestGameIntegration(unittest.TestCase):
    """Integration tests for complete game workflow"""

    @patch('random.randint', return_value=42)
    @patch('builtins.input', side_effect=['1', '42'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_complete_win_flow(self, mock_stdout, mock_input, mock_random):
        """Test complete winning game flow"""
        game.play_game()
        output = mock_stdout.getvalue()
        
        # Check all stages of the game
        self.assertIn("Welcome to Number Guessing Game!", output)
        self.assertIn("Difficulty Levels:", output)  # این در get_difficulty است
        self.assertIn("Easy mode - 15 attempts", output)
        self.assertIn("🎉 Correct! The number was 42", output)

    @patch('random.randint', return_value=42)
    @patch('builtins.input', side_effect=['3', '1', '2', '3', '4', '5'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_complete_lose_flow(self, mock_stdout, mock_input, mock_random):
        """Test complete losing game flow"""
        game.play_game()
        output = mock_stdout.getvalue()
        
        self.assertIn("Hard mode - 5 attempts", output)
        self.assertIn("💔 Game Over! No attempts left.", output)
        self.assertIn("The number was: 42", output)

if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)