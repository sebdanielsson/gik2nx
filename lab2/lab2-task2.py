# Find the value of y
import numpy as np
import time

start_time = time.time()

def calculate_y(a, b):
    a = np.array(a, dtype=np.float64)
    b = np.array(b, dtype=np.float64)

    # Check if elements in a and b are within the specified range
    if np.any(a >= 100) or np.any(b >= 100) or np.any(a <= 0) or np.any(b <= 0):
        raise ValueError("Elements in a and b must be positive integers less than 100.")

    # Ensure the length of a and b does not exceed n=50 and m=40 respectively
    if len(a) > 50 or len(b) > 40:
        raise ValueError("Length of array a must not exceed 50 and length of array b must not exceed 40.")

    # Calculate the first summation
    n = len(a)
    a_padded = np.pad(a, (0, max(0, n - len(a))), constant_values=0)[:n]
    b_padded = np.pad(b, (0, max(0, n - len(b))), constant_values=0)[:n]
    first_sum = np.sum((a_padded**4 + b_padded**2)**3)

    # Calculate the second summation
    m = len(b)
    a_padded_m = np.pad(a, (0, max(0, m - len(a))), constant_values=0)[:m]
    b_padded_m = np.pad(b, (0, max(0, m - len(b))), constant_values=0)[:m]
    second_sum = np.sum((a_padded_m**2 - b_padded_m)**2)

    # Return the sum of the two summations
    return first_sum + second_sum


# Generate random arrays for a and b with integers between 1 and 100
np.random.seed(1234)  # Set a seed for reproducibility
a = np.random.randint(1, 100, 50)
b = np.random.randint(1, 100, 40)

# Print a and b
# print(a)
# print(b)

# Calculate the result of the expression
result_with_large_numbers = calculate_y(a, b)

end_time = time.time()
execution_time = end_time - start_time

print(f"Execution time (seconds): {execution_time}")
print("Result:", result_with_large_numbers)
