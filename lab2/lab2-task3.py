# Find the value of Z
import numpy as np
import time

start_time = time.time()

def calculate_z(A1, A2, B1, B2):
    # Ensure the dimensions of A1, A2, B1, and B2 are 25x25 and the elements are positive integers less than 100
    if A1.shape != (25, 25) or A2.shape != (25, 25) or B1.shape != (25, 25) or B2.shape != (25, 25):
        raise ValueError("Dimensions of A1, A2, B1, and B2 must be 25x25.")
    if np.any(A1 >= 100) or np.any(A2 >= 100) or np.any(B1 >= 100) or np.any(B2 >= 100) or np.any(A1 <= 0) or np.any(A2 <= 0) or np.any(B1 <= 0) or np.any(B2 <= 0):
        raise ValueError("Elements in A1, A2, B1, and B2 must be positive integers less than 100.")

    # Calculate Z1, Z2, and Z
    Z1 = A1 * B1
    Z2 = A2 * B2
    Z = Z1 + Z2
    return Z


# Generate 2D matrices for A1, A2, B1, and B2 with integers between 1 and 100
np.random.seed(1234)  # Set a seed for reproducibility
A1 = np.random.randint(1, 100, (25, 25))
A2 = np.random.randint(1, 100, (25, 25))
B1 = np.random.randint(1, 100, (25, 25))
B2 = np.random.randint(1, 100, (25, 25))

# Calculate Z
Z = calculate_z(A1, A2, B1, B2)

end_time = time.time()
execution_time = end_time - start_time

print(f"Execution time (seconds): {execution_time}")
print(f"Result: {Z}")
