import random

def display_welcome():
    print("=" * 40)
    print("   Welcome to Number Guessing Game!")
    print("=" * 40)
    print("I'm thinking of a number between 1-100")
    print("Choose difficulty and start guessing!")
    print()

def get_difficulty():
    print("Difficulty Levels:")
    print("1. Easy (15 attempts)")
    print("2. Medium (10 attempts)") 
    print("3. Hard (5 attempts)")
    
    while True:
        try:
            choice = int(input("Choose (1-3): "))
            if choice == 1:
                return 15, "Easy"
            elif choice == 2:
                return 10, "Medium"
            elif choice == 3:
                return 5, "Hard"
            else:
                print("Enter 1, 2 or 3")
        except ValueError:
            print("Please enter a number")

def get_guess(attempt, max_attempts):
    while True:
        try:
            guess = int(input(f"Attempt {attempt}/{max_attempts}: "))
            if 1 <= guess <= 100:
                return guess
            print("Enter number 1-100")
        except ValueError:
            print("Enter a valid number")


def play_game():
    display_welcome()
    
    secret_number = random.randint(1, 100)
    max_attempts, difficulty = get_difficulty()
    
    print(f"\n{difficulty} mode - {max_attempts} attempts")
    print("Game starts now!\n")
    
    for attempt in range(1, max_attempts + 1):
        guess = get_guess(attempt, max_attempts)
        
        if guess == secret_number:
            print(f"\n🎉 Correct! The number was {secret_number}")
            print(f"🏆 You won in {attempt} attempts!")
            break
        elif guess < secret_number:
            print("📈 Go higher!")
        else:
            print("📉 Go lower!")
            
        # Show attempts left
        attempts_left = max_attempts - attempt
        if attempts_left > 0:
            print(f"Attempts left: {attempts_left}\n")
    else:
        # This runs only if loop completes without break
        print(f"\n💔 Game Over! No attempts left.")
        print(f"The number was: {secret_number}")

if __name__ == "__main__":
    play_game()