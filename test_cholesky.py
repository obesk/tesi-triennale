import numpy as np
import scipy
import time


def generate_positive_definite_matrix(n):
    # Create a diagonal matrix with positive entries
    A = np.diag(np.arange(1, n + 1))
    return A


a = generate_positive_definite_matrix(800)
b = np.linspace(0, 10, 800)
start = time.time_ns()
factor = scipy.linalg.cho_factor(a)
end = time.time_ns()
print(f"cho_factor time: {(end-start) / 1000000}")
start = time.time_ns()
scipy.linalg.cho_solve(factor, b)
end = time.time_ns()
print(f"cho_solve time: {(end-start) / 1000000}")