import random

def welcome():
    print("Welcom in the gesses game")

def generate_random_number(min_val=1, max_val=100):
    return random.randint(min_val, max_val)

# تولید عدد تصادفی
int_random = generate_random_number()
print(int_random)