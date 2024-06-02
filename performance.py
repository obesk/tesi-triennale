import sys
import time

using_ulab = True
try:
    from ulab import numpy as np
    from ulab import scipy
except ImportError:
    import numpy as np
    import scipy
    using_ulab = False


# Funzione per misurare il tempo
def timer(func, *args, **kwargs):
    start = time.time()
    result = func(*args, **kwargs)
    end = time.time()
    return result, (end - start) * 1000 

# Moltiplicazione di matrici
def matrix_multiplication():
    a = np.eye(100)
    b = np.ones((100, 100))
    return np.dot(a, b)

# Interpolazione
def interpolation():
    x = np.linspace(0, 10, 10)
    y = np.sin(x)
    xi = np.linspace(0, 10, 100)
    yi = np.interp(xi, x, y)
    return yi

def fft():
    x = np.linspace(0, 2 * np.pi, 128)
    y = np.sin(x)
    return np.fft.fft(y)

# Risoluzione di sistemi di equazioni lineari
def solve_linear_system():
    a = np.eye(50)
    b = np.linspace(0, 10, 50)

    if using_ulab:
        res = scipy.linalg.cho_solve(a, b)
    else:  
        factor = scipy.linalg.cho_factor(a)
        res = scipy.linalg.cho_solve(factor, b)
    return res

if using_ulab:
    prefix = "[ULAB]"
else:
    prefix = "[NUMPY]"

tests = [
    {"name": "matrix multiplication", "fun": matrix_multiplication},
    {"name": "interpolation", "fun": interpolation},
    {"name": "fft", "fun": fft},
    {"name": "linear system", "fun": solve_linear_system},
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
            n_of_tests = 1000
            result = None
            for i in range(n_of_tests):
                new_result, operation_time = timer(t["fun"])
                if result is None:
                    result = new_result
                result_comparison = result == new_result
                if using_ulab:
                    if result_comparison == True:
                        test_valid = True
                    else:
                        test_valid = False
                else:
                    test_valid = result_comparison.all()
                # if isinstance(result_comparison, np.ndarray):
                #     test_valid = check_all_true(result_comparison)
                # else:
                #     test_valid = result_comparison
                file.write(f"{t['name']},{i},{operation_time},{test_valid}\n")

if __name__ == "__main__":
    main()
