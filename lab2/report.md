# GIK2NX - Lab 2 - Report

## Table of Contents

- [GIK2NX - Lab 2 - Report](#gik2nx---lab-2---report)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Method](#method)
    - [Code](#code)
      - [Task 1 - Find the value of x.](#task-1---find-the-value-of-x)
      - [Task 2 - Find the value of y](#task-2---find-the-value-of-y)
      - [Task 3 - Find the value of Z](#task-3---find-the-value-of-z)
  - [Results](#results)
    - [Task 1](#task-1)
    - [Task 2](#task-2)
    - [Task 3](#task-3)
  - [Discussion](#discussion)
  - [Conclusion](#conclusion)

## Introduction

In this lab, we will run the code from Lab 2 on two different Azure VMs and compare the execution times. The chosen languages are Python for running the code, and PowerShell for measuring the execution times.

We will then discuss the results and calculate the speed difference between the two VMs and compare it to the difference in cost.

## Method

### Code

#### Task 1 - Find the value of x.

```python
def calculate_x(a, b):
    if not (0 <= a <= 9 and 0 <= b <= 9):
        raise ValueError("a and b must be positive integers less than 10.")
    x = a + b
    return x


a = 5
b = 7
x = calculate_x(a, b)

print(f"{x} = {a} + {b}")
```

#### Task 2 - Find the value of y

```python
import numpy as np

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
print("Result:", result_with_large_numbers)
```

#### Task 3 - Find the value of Z

```python
import numpy as np

matrix_rows = 2500
matrix_cols = 2500
integer_max = 10000

def calculate_z(A1, A2, B1, B2):
    if A1.shape != (matrix_rows, matrix_cols) or A2.shape != (matrix_rows, matrix_cols) or B1.shape != (matrix_rows, matrix_cols) or B2.shape != (matrix_rows, matrix_cols):
        raise ValueError("Dimensions of A1, A2, B1, and B2 must be ${matrix_rows}x${matrix_cols}.")
    if np.any(A1 >= integer_max) or np.any(A2 >= integer_max) or np.any(B1 >= integer_max) or np.any(B2 >= integer_max) or np.any(A1 <= 0) or np.any(A2 <= 0) or np.any(B1 <= 0) or np.any(B2 <= 0):
        raise ValueError("Elements in A1, A2, B1, and B2 must be positive integers less than ${integer_max}.")

    # Calculate Z1, Z2, and Z
    Z1 = A1 * B1
    Z2 = A2 * B2
    Z = Z1 + Z2
    return Z


np.random.seed(1234)  # Set a seed for reproducibility
A1 = np.random.randint(1, integer_max, (matrix_rows, matrix_cols))
A2 = np.random.randint(1, integer_max, (matrix_rows, matrix_cols))
B1 = np.random.randint(1, integer_max, (matrix_rows, matrix_cols))
B2 = np.random.randint(1, integer_max, (matrix_rows, matrix_cols))

# Calculate Z
Z = calculate_z(A1, A2, B1, B2)

# Print Z
print(Z)
```

After connecting to the Azure VM, we installed all of the prerequisites and cloned the repository with the code for the three tasks.

```powershell
winget install Microsoft.PowerShell
winget install Git.Git
winget install Python.Python.3.12
python -m pip install --upgrade pip
pip install numpy
git clone https://github.com/sebdanielsson/gik2nx
cd gik2nx/lab2
```

We then ran each of the tasks 10 times one by one and calculated the mean execution time to run each script. The measurements were done using the `Measure-Command` cmdlet in PowerShell.

```powershell
(Measure-Command { python .\lab2-task1.py }).TotalSeconds
(Measure-Command { python .\lab2-task2.py }).TotalSeconds
(Measure-Command { python .\lab2-task3.py }).TotalSeconds
```

## Results

### Task 1

| Run | VM1 ExecTime (s) | VM2 ExecTime (s) |
| --- | --------- | --------- |
| 1   | 0.1486903 |  |
| 2   | 0.1649746 |  |
| 3   | 0.1629312 |  |
| 4   | 0.1687515 |  |
| 5   | 0.1506248 |  |
| 6   | 0.1674121 |  |
| 7   | 0.1591185 |  |
| 8   | 0.1601762 |  |
| 9   | 0.1621312 |  |
| 10  | 0.139869  |  |

VM1 Mean Execution Time (s): 0.159
VM2 Mean Execution Time (s): 

### Task 2

| Run | VM1 ExecTime (s) | VM2 ExecTime (s) |
| --- | --------- | --------- |
| 1   | 0.393761  |  |
| 2   | 0.3940874 |  |
| 3   | 0.3803838 |  |
| 4   | 0.3699331 |  |
| 5   | 0.3600077 |  |
| 6   | 0.3671617 |  |
| 7   | 0.3496144 |  |
| 8   | 0.4015588 |  |
| 9   | 0.3604963 |  |
| 10  | 0.4039447 |  |

VM1 Mean Execution Time (s): 0.378
VM2 Mean Execution Time (s): 

### Task 3

| Run | VM1 ExecTime (s) | VM2 ExecTime (s) |
| --- | --------- | -------- |
| 1   | 1.0774044 |  |
| 2   | 1.0498384 |  |
| 3   | 0.9824914 |  |
| 4   | 1.0139454 |  |
| 5   | 1.0180805 |  |
| 6   | 0.9892987 |  |
| 7   | 1.0071994 |  |
| 8   | 1.0216969 |  |
| 9   | 0.9740818 |  |
| 10  | 1.0205213 |  |

VM1 Mean Execution Time (s): 1.016
VM2 Mean Execution Time (s): 

## Discussion

xxx

## Conclusion

xxx
