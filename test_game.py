import io
import sys
import pytest
from unittest.mock import patch
from main import welcome, generate_random_number, int_random

def test_welcome_message():
    """تست پیام خوشامدگویی"""
    captured_output = io.StringIO()
    sys.stdout = captured_output
    
    welcome()
    
    sys.stdout = sys.__stdout__
    output = captured_output.getvalue()
    
    assert "Welcom in the gesses game" in output

@patch('random.randint')
def test_generate_random_number(mock_randint):
    """تست تابع تولید عدد تصادفی"""
    mock_randint.return_value = 42
    
    result = generate_random_number(1, 100)
    
    mock_randint.assert_called_with(1, 100)
    assert result == 42

def test_global_random_number():
    """تست عدد تصادفی global"""
    assert 1 <= int_random <= 100
    assert isinstance(int_random, int)