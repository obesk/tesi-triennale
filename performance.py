import sys
import time
import json

using_ulab = True
try:
    from ulab import numpy as np
    from ulab import scipy
except ImportError:
    import numpy as np
    import scipy
    using_ulab = False


def timer(func, *args, **kwargs):
    start = time.time_ns()
    result = func(*args, **kwargs)
    end = time.time_ns()
    return result, (end - start) / 1000000

def matrix_multiplication(a, b):
    return np.dot(a, b)

def interpolation(x, xi):
    y = np.sin(x)
    yi = np.interp(xi, x, y)
    return yi

def fft(x):
    y = np.sin(x)
    return np.fft.fft(y)

# Risoluzione di sistemi di equazioni lineari
def solve_linear_system(a, b):
    if using_ulab:
        res = scipy.linalg.cho_solve(a, b)
    else:  
        factor = scipy.linalg.cho_factor(a)
        res = scipy.linalg.cho_solve(factor, b)
    return res

def generate_positive_definite_matrix(n):
    # Create a diagonal matrix with positive entries
    A = np.diag(np.arange(1, n + 1))
    return A


if using_ulab:
    prefix = "[ULAB]"
else:
    prefix = "[NUMPY]"

tests = [
    {
        "name": "matrix multiplication",
        "fun": matrix_multiplication, 
        "kwargs": { "a": np.full((200, 200), 21), "b": np.full((200, 200), 65)},
    },
    {
        "name": "interpolation",
        "fun": interpolation,
        "kwargs": { "x": np.linspace(0, 200, 100000), "xi": np.linspace(0, 10, 100000)}
    },
    {
        "name": "fft",
        "fun" : fft,
        "kwargs": { "x": np.linspace(0, 2 * np.pi, 65536)},
    },
    {
        "name": "linear system",
        "fun": solve_linear_system,
        "kwargs": { "a": generate_positive_definite_matrix(800), "b": np.linspace(0, 10, 800)}
    },
]


# ulab doesn't support the all() function
def check_all_true(matrix):
    for elem in matrix:
        print(elem)
        if not elem:
            return False
    return True

def main():
    if (len(sys.argv) >= 2):
        testfile = sys.argv[1]
        print(testfile)
    else:
        testfile = f"times/{prefix} times.csv"
    with open(testfile, "w") as file:
        file.write("test name,id,time,valid\n")
        for t in tests:
            n_of_tests = 100
            results = []
            for i in range(n_of_tests):
                result, operation_time = timer(t["fun"], **t.get("kwargs", {}))
                results.append(convert_to_list(result))
                file.write(f"{t['name']},{i},{operation_time}\n")

            with open(f"results/{t['name']}.json", "w") as f:
                json.dump(results, f)


def convert_to_list(result):
    if isinstance(result, np.ndarray):
        return result.tolist()
    elif isinstance(result, tuple):
        return [convert_to_list(item) for item in result]
    else:
        return result

if __name__ == "__main__":
    main()
