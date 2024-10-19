#AI generated for explorative purposes

<<<<<<< HEAD
from functools import cache, lru_cache
#from pyJoules.device.rapl_device import RaplPackageDomain
#from pyJoules.energy_meter import measure_energy
import itertools


# Basic Implementation
#@measure_energy(domains=[RaplPackageDomain(0)])
=======
from functools import cache, lru_cache, wraps
import itertools
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
>>>>>>> 82983cb (code running on raspberry PI 4)
def generate_permutations(tup: tuple) -> tuple:
    return list(itertools.permutations(tup))

# Using functools.cache (Python 3.9+)
<<<<<<< HEAD
#@measure_energy(domains=[RaplPackageDomain(0)])
=======
>>>>>>> 82983cb (code running on raspberry PI 4)
@cache
def generate_permutations_cache(tup: tuple) -> tuple:
    return list(itertools.permutations(tup))

# Using functools.lru_cache
<<<<<<< HEAD
#@measure_energy(domains=[RaplPackageDomain(0)])
=======
>>>>>>> 82983cb (code running on raspberry PI 4)
@lru_cache(maxsize=None)
def generate_permutations_lru_cache(tup: tuple) -> tuple:
    return list(itertools.permutations(tup))


if __name__ == '__main__':
    # Example Usage
<<<<<<< HEAD
    tup = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)

    print(generate_permutations(tup))
    print(generate_permutations_cache(tup))
    print(generate_permutations_lru_cache(tup))
=======
    tup = (1, 2, 3, 4, 5, 6, 7)

    print(measure_time(generate_permutations, tup))
    
    print(measure_time(generate_permutations_cache, tup))
    print(measure_time(generate_permutations_cache, tup))

    print(measure_time(generate_permutations_lru_cache, tup))
    print(measure_time(generate_permutations_lru_cache, tup))
    
    assert generate_permutations(tup) == generate_permutations_cache(tup) == generate_permutations_lru_cache(tup)

>>>>>>> 82983cb (code running on raspberry PI 4)
