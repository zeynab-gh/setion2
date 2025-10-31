import unittest
from unittest.mock import patch
import random
from io import StringIO
import sys

# Import the main game file
import number_guessing_game as game

class TestNumberGuessingGame(unittest.TestCase):

    def setUp(self):
        """Setup before each test"""
        self.held_output = StringIO()

    def tearDown(self):
        """Cleanup after each test"""
        self.held_output.close()

    # Welcome message tests
    def test_display_welcome(self):
        """Test welcome message display"""
        with patch('sys.stdout', new=StringIO()) as fake_output:
            game.display_welcome()
            output = fake_output.getvalue()
            
            self.assertIn("Welcome to the Number Guessing Game!", output)
            self.assertIn("Rules:", output)
            self.assertIn("I'm thinking of a number between 1 and 100", output)

    # Difficulty selection tests
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

    @patch('builtins.input', side_effect=['0', '4', '2'])
    def test_get_difficulty_invalid_then_valid(self, mock_input):
        """Test invalid then valid difficulty selection"""
        attempts, difficulty = game.get_difficulty()
        self.assertEqual(attempts, 10)
        self.assertEqual(difficulty, "Medium")

    # Guess input tests
    @patch('builtins.input', side_effect=['50'])
    def test_get_guess_valid(self, mock_input):
        """Test valid guess input"""
        guess = game.get_guess(1, 10)
        self.assertEqual(guess, 50)

    @patch('builtins.input', side_effect=['0', '101', '50'])
    def test_get_guess_invalid_then_valid(self, mock_input):
        """Test invalid then valid guess"""
        guess = game.get_guess(1, 10)
        self.assertEqual(guess, 50)

    @patch('builtins.input', side_effect=['abc', '50'])
    def test_get_guess_invalid_input_then_valid(self, mock_input):
        """Test invalid input then valid guess"""
        guess = game.get_guess(1, 10)
        self.assertEqual(guess, 50)

    # Game flow tests
    @patch('random.randint', return_value=42)
    @patch('builtins.input', side_effect=['1', '42'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_play_game_win_first_try(self, mock_stdout, mock_input, mock_random):
        """Test winning on first try"""
        game.play_game()
        output = mock_stdout.getvalue()
        self.assertIn("Congratulations! You guessed the number 42 correctly!", output)
        self.assertIn("It took you 1 attempts to win!", output)

    @patch('random.randint', return_value=42)
    @patch('builtins.input', side_effect=['1', '10', '20', '30', '40', '42'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_play_game_win_multiple_attempts(self, mock_stdout, mock_input, mock_random):
        """Test winning after multiple attempts"""
        game.play_game()
        output = mock_stdout.getvalue()
        self.assertIn("Congratulations! You guessed the number 42 correctly!", output)
        self.assertIn("The number is HIGHER than your guess.", output)

    @patch('random.randint', return_value=42)
    @patch('builtins.input', side_effect=['3', '50', '45', '43', '41', '44'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_play_game_lose(self, mock_stdout, mock_input, mock_random):
        """Test losing the game"""
        game.play_game()
        output = mock_stdout.getvalue()
        self.assertIn("Game Over! You've used all 5 attempts.", output)
        self.assertIn("The secret number was: 42", output)

    @patch('random.randint', return_value=42)
    @patch('builtins.input', side_effect=['1', '30', '50', '42'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_play_game_hints(self, mock_stdout, mock_input, mock_random):
        """Test high/low hints functionality"""
        game.play_game()
        output = mock_stdout.getvalue()
        self.assertIn("The number is HIGHER than your guess.", output)
        self.assertIn("The number is LOWER than your guess.", output)

    # Random number tests
    def test_random_number_range(self):
        """Test random number generation range"""
        random_numbers = [random.randint(1, 100) for _ in range(1000)]
        self.assertTrue(all(1 <= num <= 100 for num in random_numbers))
        self.assertIn(1, random_numbers)
        self.assertIn(100, random_numbers)

class TestGameIntegration(unittest.TestCase):
    """Integration tests for complete game flow"""

    @patch('random.randint', return_value=42)
    @patch('builtins.input', side_effect=['1', '42'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_complete_win_flow(self, mock_stdout, mock_input, mock_random):
        """Test complete winning flow"""
        game.play_game()
        output = mock_stdout.getvalue()
        
        self.assertIn("Welcome to the Number Guessing Game!", output)
        self.assertIn("Choose your difficulty level:", output)
        self.assertIn("You've chosen Easy difficulty", output)
        self.assertIn("Congratulations!", output)

    @patch('random.randint', return_value=42)
    @patch('builtins.input', side_effect=['3', '10', '20', '30', '40', '50'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_complete_lose_flow(self, mock_stdout, mock_input, mock_random):
        """Test complete losing flow"""
        game.play_game()
        output = mock_stdout.getvalue()
        
        self.assertIn("Game Over!", output)
        self.assertIn("The secret number was: 42", output)

if __name__ == '__main__':
    # Run tests with detailed output
    unittest.main(verbosity=2)