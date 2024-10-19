#AI generated for explorative purposes

<<<<<<< HEAD
from functools import cache, lru_cache
#from pyJoules.device.rapl_device import RaplPackageDomain
#from pyJoules.energy_meter import measure_energy
=======
from functools import cache, lru_cache, wraps
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
>>>>>>> 82983cb (code running on raspberry PI 4)


# Basic Implementation
def tower_of_hanoi(n: int, source: str, target: str, auxiliary: str) -> None:
    if n == 1:
<<<<<<< HEAD
        print(f"Move disk 1 from {source} to {target}")
        return 
    tower_of_hanoi(n-1, source, auxiliary, target)
    print(f"Move disk {n} from {source} to {target}")
=======
        # print(f"Move disk 1 from {source} to {target}")
        return 
    tower_of_hanoi(n-1, source, auxiliary, target)
    # print(f"Move disk {n} from {source} to {target}")
>>>>>>> 82983cb (code running on raspberry PI 4)
    tower_of_hanoi(n-1, auxiliary, target, source)
    
# Using functools.cache (Python 3.9+)
@cache
def tower_of_hanoi_cache(n: int, source: str, target: str, auxiliary: str) -> None:
    if n == 1:
<<<<<<< HEAD
        print(f"Move disk 1 from {source} to {target}")
        return
    tower_of_hanoi_cache(n-1, source, auxiliary, target)
    print(f"Move disk {n} from {source} to {target}")
=======
        # print(f"Move disk 1 from {source} to {target}")
        return
    tower_of_hanoi_cache(n-1, source, auxiliary, target)
    # print(f"Move disk {n} from {source} to {target}")
>>>>>>> 82983cb (code running on raspberry PI 4)
    tower_of_hanoi_cache(n-1, auxiliary, target, source)
    
# Using functools.lru_cache
@lru_cache(maxsize=None)
def tower_of_hanoi_lru_cache(n: int, source: str, target: str, auxiliary: str) -> None:
    if n == 1:
<<<<<<< HEAD
        print(f"Move disk 1 from {source} to {target}")
        return
    tower_of_hanoi_lru_cache(n-1, source, auxiliary, target)
    print(f"Move disk {n} from {source} to {target}")
=======
        # print(f"Move disk 1 from {source} to {target}")
        return
    tower_of_hanoi_lru_cache(n-1, source, auxiliary, target)
    # print(f"Move disk {n} from {source} to {target}")
>>>>>>> 82983cb (code running on raspberry PI 4)
    tower_of_hanoi_lru_cache(n-1, auxiliary, target, source)
    
if __name__ == '__main__':
    # Example usage
<<<<<<< HEAD
    n = 3
=======
    n = 25
>>>>>>> 82983cb (code running on raspberry PI 4)
    source = "A"
    target = "C"
    auxiliary = "B"

    tower_of_hanoi(n, source, target, auxiliary)
<<<<<<< HEAD
    tower_of_hanoi_cache(n, source, target, auxiliary)
    tower_of_hanoi_lru_cache(n, source, target, auxiliary)
=======
    
    print(measure_time(tower_of_hanoi, n, source, target, auxiliary))

    print(measure_time(tower_of_hanoi_cache, n, source, target, auxiliary))
    
    print(measure_time(tower_of_hanoi_lru_cache, n, source, target, auxiliary))
    
    assert tower_of_hanoi(n, source, target, auxiliary) == tower_of_hanoi_cache(n, source, target, auxiliary) == tower_of_hanoi_lru_cache(n, source, target, auxiliary)

>>>>>>> 82983cb (code running on raspberry PI 4)
