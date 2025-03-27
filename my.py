# * * * * * *
# 1. **Create a NumPy Array:** Create a 1D array of numbers from 0 to 9.
import numpy as np
import pandas as pd

arr = np.array([20, 441, 24, 13, 4, 54, 64, 123127, 81])

# * * * * * *
# 2. **Array Properties:** Print the shape, size, and data type of an array.
# print(f"shape: {arr.shape}")
# print(f"size: {arr.size}")
# print(f"type: {type(arr)}")

# * * * * * *
# 3. **Reshape an Array:** Convert a 1D array of size 9 into a 3x3 matrix.
# reshaped_arr = np.reshape(arr,(3,3))
# print(reshaped_arr)

# * * * * * *
# 4. **Indexing & Slicing:** Extract every second element from an array.
# print(arr[::2])

# * * * * * *
# 5. **Boolean Indexing:** Filter out numbers greater than 5 from an array.
# filtered_arr = []
# for item in arr:
#     if item > 5:
#         filtered_arr.append(item)

# print(np.array(filtered_arr))

# * * * * * *
# **Element-wise Operations:** Multiply all elements of an array by 2.
# temp_arr = []
# for item in arr:
#     item*=2
#     temp_arr.append(item)
# print(np.array(temp_arr))

# * * * * * *
# 7. **Matrix Multiplication:** Perform matrix multiplication on two random matrices.

# matrix1 = np.random.randint(1, 100, (3, 3))
# matrix2 = np.random.randint(1, 100, (3, 3))

# print("Matrix 1:\n", matrix1)
# print("\nMatrix 2:\n", matrix2)

# matrix3 = matrix1 * matrix2
# print("\nmult matrix :\n", matrix3)

# * * * * * *
# 8. **Identity Matrix:** Create a 4x4 identity matrix.
# identity_matrix = np.eye(4)
# print(identity_matrix)

# * * * * * *
# 9. **Random Number Generation:** Generate a 5x5 array of random numbers between 0 and 1.
# matrix_5x5 = np.random.rand(5, 5)
# print(matrix_5x5)

# * * * * * *
# **Sorting an Array:** Sort a NumPy array in ascending order.
# sorted_arr = np.sort(arr)
# print(sorted_arr)

# * * * * * *
# 11. **Concatenation:** Concatenate two 1D arrays.
# concat_arr = np.concat([arr, arr_2])
# print(concat_arr)

# * * * * * *
# 12. **Stacking:** Stack two 1D arrays vertically and horizontally.
# vstacked_arr = np.vstack([arr, arr_2])
# hstacked_arr = np.hstack([arr, arr_2])

# print(f"array 1: {arr}, array 2: {arr_2}")
# print("******")
# print(f"{vstacked_arr} vertical")
# print("******")
# print(f"{hstacked_arr} horizontal")

# * * * * * *
# 13. **Statistics:** Compute the mean, median, and standard deviation of an array.
