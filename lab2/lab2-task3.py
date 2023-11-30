# Find the value of Z
import numpy as np

matrix_rows = 250
matrix_cols = 250


def calculate_z(A1, A2, B1, B2):
    if (
        A1.shape != (matrix_rows, matrix_cols)
        or A2.shape != (matrix_rows, matrix_cols)
        or B1.shape != (matrix_rows, matrix_cols)
        or B2.shape != (matrix_rows, matrix_cols)
    ):
        raise ValueError(
            "Dimensions of A1, A2, B1, and B2 must be ${matrix_rows}x${matrix_cols}."
        )
    if (
        np.any(A1 >= 100)
        or np.any(A2 >= 100)
        or np.any(B1 >= 100)
        or np.any(B2 >= 100)
        or np.any(A1 <= 0)
        or np.any(A2 <= 0)
        or np.any(B1 <= 0)
        or np.any(B2 <= 0)
    ):
        raise ValueError(
            "Elements in A1, A2, B1, and B2 must be positive integers less than 100."
        )

    # Calculate Z1, Z2, and Z
    Z1 = A1 * B1
    Z2 = A2 * B2
    Z = Z1 + Z2
    return Z


# Generate 2D matrices for A1, A2, B1, and B2 with integers between 1 and 100
np.random.seed(1234)  # Set a seed for reproducibility
A1 = np.random.randint(1, 100, (matrix_rows, matrix_cols))
A2 = np.random.randint(1, 100, (matrix_rows, matrix_cols))
B1 = np.random.randint(1, 100, (matrix_rows, matrix_cols))
B2 = np.random.randint(1, 100, (matrix_rows, matrix_cols))

# Calculate Z
Z = calculate_z(A1, A2, B1, B2)

# Print Z
print(Z)
