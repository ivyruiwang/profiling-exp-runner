#AI generated for explorative purposes

<<<<<<< HEAD
from functools import lru_cache, cache
#from pyJoules.device.rapl_device import RaplPackageDomain
#from pyJoules.energy_meter import measure_energy
import numpy as np


# Basic Implementation
#@measure_energy(domains=[RaplPackageDomain(0)])
def convolve2d(matrix: np.ndarray, kernel: np.ndarray) -> np.ndarray:
=======
from functools import cache, lru_cache, wraps
import numpy as np
from time import perf_counter

def timer(func, *args, **kwargs):
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = perf_counter()
        print(f'Starting {func.__name__} at {start}')   # 1
        result = func(*args, **kwargs)
        end = perf_counter()
        print(f'Finished {func.__name__} at {end}')     # 3
        print(f"Elapsed time: {end - start}")           # 4
        return result                                   # 5                
    return wrapper

@timer
def measure_time(func: callable, *args, **kwargs):
    print(f"Calling {func.__name__} with args: {args}")  # 2
    return func(*args, **kwargs)


# Basic Implementation
def convolve2d(matrix_tuple: tuple, kernel_tuple: tuple) -> np.ndarray:
    matrix = np.array(matrix_tuple)
    kernel = np.array(kernel_tuple)
>>>>>>> 82983cb (code running on raspberry PI 4)
    m, n = matrix.shape
    km, kn = kernel.shape
    output = np.zeros((m - km + 1, n - kn + 1))
    
    def compute_element(i: int, j: int) -> float:
        return np.sum(matrix[i:i+km, j:j+kn] * kernel)
    
    for i in range(m - km + 1):
        for j in range(n - kn + 1):
            output[i, j] = compute_element(i, j)
    
    return output

# Using functools.cache (Python 3.9+)
<<<<<<< HEAD
#@measure_energy(domains=[RaplPackageDomain(0)])
def convolve2d_cache(matrix: np.ndarray, kernel: np.ndarray) -> np.ndarray:
=======
@cache
def convolve2d_cache(matrix_tuple: tuple, kernel_tuple: tuple) -> np.ndarray:
    matrix = np.array(matrix_tuple)
    kernel = np.array(kernel_tuple)
>>>>>>> 82983cb (code running on raspberry PI 4)
    m, n = matrix.shape
    km, kn = kernel.shape
    output = np.zeros((m - km + 1, n - kn + 1))
    
<<<<<<< HEAD
    @cache
=======
>>>>>>> 82983cb (code running on raspberry PI 4)
    def compute_element(i: int, j: int) -> float:
        return np.sum(matrix[i:i+km, j:j+kn] * kernel)
    
    for i in range(m - km + 1):
        for j in range(n - kn + 1):
            output[i, j] = compute_element(i, j)
    
    return output

# Using functools.lru_cache
<<<<<<< HEAD
#@measure_energy(domains=[RaplPackageDomain(0)])
def convolve2d_lru_cache(matrix: np.ndarray, kernel: np.ndarray) -> np.ndarray:
=======
@lru_cache(maxsize=None)
def convolve2d_lru_cache(matrix_tuple: tuple, kernel_tuple: tuple) -> np.ndarray:
    matrix = np.array(matrix_tuple)
    kernel = np.array(kernel_tuple)
>>>>>>> 82983cb (code running on raspberry PI 4)
    m, n = matrix.shape
    km, kn = kernel.shape
    output = np.zeros((m - km + 1, n - kn + 1))
    
<<<<<<< HEAD
    @lru_cache(maxsize=None)
=======
>>>>>>> 82983cb (code running on raspberry PI 4)
    def compute_element(i: int, j: int) -> float:
        return np.sum(matrix[i:i+km, j:j+kn] * kernel)
    
    for i in range(m - km + 1):
        for j in range(n - kn + 1):
            output[i, j] = compute_element(i, j)
    
    return output


if __name__ == '__main__':
    # Example usage
<<<<<<< HEAD
    matrix = np.random.rand(1080, 1920)
    kernel = np.random.rand(3, 3)

    print("Basic Implementation:\n", convolve2d(matrix, kernel))
    print("Using functools.cache:\n", convolve2d_cache(matrix, kernel))
    print("Using functools.lru_cache:\n", convolve2d_lru_cache(matrix, kernel))
=======
    matrix = np.random.rand(33, 33)
    kernel = np.random.rand(3, 3)
    
    matrix_tuple = tuple(map(tuple, matrix))
    kernel_tuple = tuple(map(tuple, kernel))

    print(measure_time(convolve2d, matrix_tuple, kernel_tuple))
    
    print(measure_time(convolve2d_cache, matrix_tuple, kernel_tuple))
    print(measure_time(convolve2d_cache, matrix_tuple, kernel_tuple))


    print(measure_time(convolve2d_lru_cache, matrix_tuple, kernel_tuple))
    print(measure_time(convolve2d_lru_cache, matrix_tuple, kernel_tuple))

    assert np.allclose(convolve2d(matrix_tuple, kernel_tuple), convolve2d_cache(matrix_tuple, kernel_tuple)) and np.allclose(convolve2d(matrix_tuple, kernel_tuple), convolve2d_lru_cache(matrix_tuple, kernel_tuple))
>>>>>>> 82983cb (code running on raspberry PI 4)
