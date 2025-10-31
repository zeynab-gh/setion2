import unittest
from unittest.mock import patch
import random
from io import StringIO
import sys

# ایمپورت کردن فایل اصلی بازی
import number_guessing_game as game

class TestNumberGuessingGame(unittest.TestCase):

    def setUp(self):
        """آماده‌سازی قبل از هر تست"""
        self.held_output = StringIO()

    def tearDown(self):
        """پاکسازی بعد از هر تست"""
        self.held_output.close()

    def test_display_welcome(self):
        """تست نمایش پیام خوش‌آمدگویی"""
        with patch('sys.stdout', new=StringIO()) as fake_output:
            game.display_welcome()
            output = fake_output.getvalue()
            
            self.assertIn("Welcome to the Number Guessing Game!", output)
            self.assertIn("Rules:", output)
            self.assertIn("I'm thinking of a number between 1 and 100", output)

    @patch('builtins.input', side_effect=['1'])
    def test_get_difficulty_easy(self, mock_input):
        """تست انتخاب سطح آسان"""
        attempts, difficulty = game.get_difficulty()
        self.assertEqual(attempts, 15)
        self.assertEqual(difficulty, "Easy")

    @patch('builtins.input', side_effect=['2'])
    def test_get_difficulty_medium(self, mock_input):
        """تست انتخاب سطح متوسط"""
        attempts, difficulty = game.get_difficulty()
        self.assertEqual(attempts, 10)
        self.assertEqual(difficulty, "Medium")

    @patch('builtins.input', side_effect=['3'])
    def test_get_difficulty_hard(self, mock_input):
        """تست انتخاب سطح سخت"""
        attempts, difficulty = game.get_difficulty()
        self.assertEqual(attempts, 5)
        self.assertEqual(difficulty, "Hard")

    @patch('builtins.input', side_effect=['0', '4', '2'])
    def test_get_difficulty_invalid_then_valid(self, mock_input):
        """تست انتخاب سطح نامعتبر و سپس معتبر"""
        attempts, difficulty = game.get_difficulty()
        self.assertEqual(attempts, 10)
        self.assertEqual(difficulty, "Medium")

    @patch('builtins.input', side_effect=['abc', '2'])
    def test_get_difficulty_invalid_input_then_valid(self, mock_input):
        """تست ورودی نامعتبر و سپس معتبر"""
        attempts, difficulty = game.get_difficulty()
        self.assertEqual(attempts, 10)
        self.assertEqual(difficulty, "Medium")

    @patch('builtins.input', side_effect=['50'])
    def test_get_guess_valid(self, mock_input):
        """تست حدس معتبر"""
        guess = game.get_guess(1, 10)
        self.assertEqual(guess, 50)

    @patch('builtins.input', side_effect=['0', '101', '50'])
    def test_get_guess_invalid_then_valid(self, mock_input):
        """تست حدس نامعتبر و سپس معتبر"""
        guess = game.get_guess(1, 10)
        self.assertEqual(guess, 50)

    @patch('builtins.input', side_effect=['abc', '50'])
    def test_get_guess_invalid_input_then_valid(self, mock_input):
        """تست ورودی نامعتبر و سپس معتبر برای حدس"""
        guess = game.get_guess(1, 10)
        self.assertEqual(guess, 50)

    @patch('random.randint', return_value=42)
    @patch('builtins.input', side_effect=['1', '42'])  # Easy difficulty, then correct guess
    @patch('sys.stdout', new_callable=StringIO)
    def test_play_game_win_first_try(self, mock_stdout, mock_input, mock_random):
        """تست برنده شدن در اولین حدس"""
        game.play_game()
        output = mock_stdout.getvalue()
        self.assertIn("Congratulations! You guessed the number 42 correctly!", output)
        self.assertIn("It took you 1 attempts to win!", output)

    @patch('random.randint', return_value=42)
    @patch('builtins.input', side_effect=['1', '10', '20', '30', '40', '42'])  # Multiple guesses
    @patch('sys.stdout', new_callable=StringIO)
    def test_play_game_win_multiple_attempts(self, mock_stdout, mock_input, mock_random):
        """تست برنده شدن پس از چندین حدس"""
        game.play_game()
        output = mock_stdout.getvalue()
        self.assertIn("Congratulations! You guessed the number 42 correctly!", output)
        self.assertIn("The number is HIGHER than your guess.", output)

    @patch('random.randint', return_value=42)
    @patch('builtins.input', side_effect=['3', '50', '45', '43', '41', '44'])  # Hard difficulty, all wrong guesses
    @patch('sys.stdout', new_callable=StringIO)
    def test_play_game_lose(self, mock_stdout, mock_input, mock_random):
        """تست باختن در بازی"""
        game.play_game()
        output = mock_stdout.getvalue()
        self.assertIn("Game Over! You've used all 5 attempts.", output)
        self.assertIn("The secret number was: 42", output)

    @patch('random.randint', return_value=42)
    @patch('builtins.input', side_effect=['1', '30', '50', '42'])  # Test high/low hints
    @patch('sys.stdout', new_callable=StringIO)
    def test_play_game_hints(self, mock_stdout, mock_input, mock_random):
        """تست راهنمایی‌های بالا/پایین"""
        game.play_game()
        output = mock_stdout.getvalue()
        self.assertIn("The number is HIGHER than your guess.", output)  # For guess 30
        self.assertIn("The number is LOWER than your guess.", output)   # For guess 50

    @patch('random.randint', return_value=42)
    @patch('builtins.input', side_effect=['2', '42'])  # Medium difficulty
    @patch('sys.stdout', new_callable=StringIO)
    def test_play_game_difficulty_display(self, mock_stdout, mock_input, mock_random):
        """تست نمایش سطح دشواری"""
        game.play_game()
        output = mock_stdout.getvalue()
        self.assertIn("You've chosen Medium difficulty", output)
        self.assertIn("You have 10 attempts", output)

    def test_random_number_range(self):
        """تست محدوده اعداد تصادفی"""
        random_numbers = [random.randint(1, 100) for _ in range(1000)]
        self.assertTrue(all(1 <= num <= 100 for num in random_numbers))
        self.assertIn(1, random_numbers)
        self.assertIn(100, random_numbers)

    @patch('random.randint', return_value=42)
    @patch('builtins.input', side_effect=['1', '42'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_play_game_emoji_display(self, mock_stdout, mock_input, mock_random):
        """تست نمایش ایموجی‌ها"""
        game.play_game()
        output = mock_stdout.getvalue()
        # فقط بررسی می‌کنیم که بازی بدون خطا اجرا می‌شود
        self.assertIn("Congratulations!", output)

class TestGameIntegration(unittest.TestCase):
    """تست‌های یکپارچگی برای کل بازی"""

    @patch('random.randint', return_value=42)
    @patch('builtins.input', side_effect=['1', '42'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_complete_win_flow(self, mock_stdout, mock_input, mock_random):
        """تست جریان کامل برنده شدن"""
        game.play_game()
        output = mock_stdout.getvalue()
        
        # بررسی مراحل مختلف بازی
        self.assertIn("Welcome to the Number Guessing Game!", output)
        self.assertIn("Choose your difficulty level:", output)
        self.assertIn("You've chosen Easy difficulty", output)
        self.assertIn("Congratulations!", output)

    @patch('random.randint', return_value=42)
    @patch('builtins.input', side_effect=['3', '10', '20', '30', '40', '50'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_complete_lose_flow(self, mock_stdout, mock_input, mock_random):
        """تست جریان کامل باختن"""
        game.play_game()
        output = mock_stdout.getvalue()
        
        self.assertIn("Game Over!", output)
        self.assertIn("The secret number was: 42", output)

if __name__ == '__main__':
    # اجرای تست‌ها
    unittest.main(verbosity=2)