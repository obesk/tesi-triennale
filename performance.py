import os
import sys
import time

using_ulab = True
try:
    from ulab import numpy as np
    from ulab import scipy
    import json

except ImportError:
    import numpy as np
    import scipy
    import pickle
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


def main():
    if (len(sys.argv) >= 2):
        testfile = f"times/{sys.argv[1]}.csv"
        resultfile = f"results/{sys.argv[1]}.pkl"
    else:
        testfile = f"times/{prefix} times.csv"
    results = {}
    with open(testfile, "w") as test_f:
        test_f.write("test name,id,time\n")
        for t in tests:
            print(f"Running test {t['name']}")
            n_of_tests = 100
            for i in range(n_of_tests):
                result, operation_time = timer(t["fun"], **t.get("kwargs", {}))
                if i == 0:
                    results[t["name"]] = convert_to_list(result)
                test_f.write(f"{t['name']},{i},{operation_time}\n")

    print("Saving results")
    with open(resultfile, "wb") as result_f:
        if using_ulab:
            json.dump(results, result_f)
        else:
            pickle.dump(results, result_f)

def convert_to_list(result):
    if isinstance(result, np.ndarray):
        return result.tolist()
    elif isinstance(result, tuple):
        return [convert_to_list(item) for item in result]
    elif isinstance(result, complex):
        return [result.real, result.imag]
    else:
        return result



if __name__ == "__main__":
    main()
