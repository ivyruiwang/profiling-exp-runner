#AI generated for explorative purposes

<<<<<<< HEAD
from functools import cache, lru_cache
import numpy as np
#from pyJoules.device.rapl_device import RaplPackageDomain
#from pyJoules.energy_meter import measure_energy

# Basic Implementation
#@measure_energy(domains=[RaplPackageDomain(0)])
def pca(X: np.ndarray, num_components: int) -> np.ndarray:
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
def pca(X_tuple: tuple, num_components: int) -> np.ndarray:
    X = np.array(X_tuple)  # Convert tuple back to numpy array
>>>>>>> 82983cb (code running on raspberry PI 4)
    X_meaned = X - np.mean(X, axis=0)
    cov_matrix = np.cov(X_meaned, rowvar=False)
    eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)
    sorted_index = np.argsort(eigenvalues)[::-1]
    sorted_eigenvalues = eigenvalues[sorted_index]
    sorted_eigenvectors = eigenvectors[:, sorted_index]
    eigenvector_subset = sorted_eigenvectors[:, 0:num_components]
    X_reduced = np.dot(eigenvector_subset.transpose(), X_meaned.transpose()).transpose()
    return X_reduced


# Using functools.cache (Python 3.9+)
<<<<<<< HEAD
#@measure_energy(domains=[RaplPackageDomain(0)])
=======
>>>>>>> 82983cb (code running on raspberry PI 4)
@cache
def pca_cache(X_tuple: tuple, num_components: int) -> np.ndarray:
    X = np.array(X_tuple)  # Convert tuple back to numpy array
    X_meaned = X - np.mean(X, axis=0)
    cov_matrix = np.cov(X_meaned, rowvar=False)
    eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)
    sorted_index = np.argsort(eigenvalues)[::-1]
    sorted_eigenvalues = eigenvalues[sorted_index]
    sorted_eigenvectors = eigenvectors[:, sorted_index]
    eigenvector_subset = sorted_eigenvectors[:, 0:num_components]
    X_reduced = np.dot(eigenvector_subset.transpose(), X_meaned.transpose()).transpose()
    return X_reduced

# Using functools.lru_cache
<<<<<<< HEAD
#@measure_energy(domains=[RaplPackageDomain(0)])
=======
>>>>>>> 82983cb (code running on raspberry PI 4)
@lru_cache(maxsize=None)
def pca_lru_cache(X_tuple: tuple, num_components: int) -> np.ndarray:
    X = np.array(X_tuple)  # Convert tuple back to numpy array
    X_meaned = X - np.mean(X, axis=0)
    cov_matrix = np.cov(X_meaned, rowvar=False)
    eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)
    sorted_index = np.argsort(eigenvalues)[::-1]
    sorted_eigenvalues = eigenvalues[sorted_index]
    sorted_eigenvectors = eigenvectors[:, sorted_index]
    eigenvector_subset = sorted_eigenvectors[:, 0:num_components]
    X_reduced = np.dot(eigenvector_subset.transpose(), X_meaned.transpose()).transpose()
    return X_reduced


if __name__ == '__main__':
    # Example usage
<<<<<<< HEAD
    X = np.random.rand(1000, 100)
=======
    X = np.random.rand(100, 100)
>>>>>>> 82983cb (code running on raspberry PI 4)
    num_components = 10

    # Convert numpy array to tuple for caching
    X_tuple = tuple(map(tuple, X))  # Convert 2D array to tuple of tuples

<<<<<<< HEAD
    print('normal:', pca(X, num_components))
    print('cache:',pca_cache(X_tuple, num_components))
    print('lru_cache:', pca_lru_cache(X_tuple, num_components))
=======
    print(measure_time(pca, X_tuple, num_components))
    
    print(measure_time(pca_cache, X_tuple, num_components))
    print(measure_time(pca_cache, X_tuple, num_components))

    print(measure_time(pca_lru_cache, X_tuple, num_components))
    print(measure_time(pca_lru_cache, X_tuple, num_components))

    assert np.allclose(pca(X_tuple, num_components), pca_cache(X_tuple, num_components)) and np.allclose(pca(X_tuple, num_components), pca_lru_cache(X_tuple, num_components))

>>>>>>> 82983cb (code running on raspberry PI 4)
