# Find the value of x
def calculate_x(a, b):
    if not (0 <= a <= 9 and 0 <= b <= 9):
        raise ValueError("a and b must be positive integers less than 10.")
    x = a + b
    return x


a = 5
b = 7
x = calculate_x(a, b)

print(f"{x} = {a} + {b}")
