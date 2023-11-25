# Find the value of x
import time

start_time = time.time()
def calculate_x(a, b):
    if not (0 <= a <= 9 and 0 <= b <= 9):
        raise ValueError("a and b must be positive integers less than 10.")
    x = a + b
    return x


a = 5
b = 7
x = calculate_x(a, b)

end_time = time.time()
execution_time = end_time - start_time

print(f"Execution time (seconds): {execution_time}")

print(f"Result: {x} = {a} + {b}")
