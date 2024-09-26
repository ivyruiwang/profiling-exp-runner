#AI generated for explorative purposes

from functools import cache, lru_cache
#from pyJoules.device.rapl_device import RaplPackageDomain
#from pyJoules.energy_meter import measure_energy

# Basic Implementation
#@measure_energy(domains=[RaplPackageDomain(0)])
def knapsack_basic(weights: list[int], values: list[int], capacity: int) -> int:
    n = len(weights)
    
    def knapsack_recursive(i: int, remaining_capacity: int) -> int:
        if i < 0 or remaining_capacity <= 0:
            return 0
        if weights[i] > remaining_capacity:
            return knapsack_recursive(i - 1, remaining_capacity)
        else:
            return max(knapsack_recursive(i - 1, remaining_capacity),
                       values[i] + knapsack_recursive(i - 1, remaining_capacity - weights[i]))
    
    return knapsack_recursive(n - 1, capacity)

# Using functools.cache (Python 3.9+)
#@measure_energy(domains=[RaplPackageDomain(0)])
def knapsack_cache(weights: list[int], values: list[int], capacity: int) -> int:
    n = len(weights)
    
    @cache
    def knapsack_recursive(i: int, remaining_capacity: int) -> int:
        if i < 0 or remaining_capacity <= 0:
            return 0
        if weights[i] > remaining_capacity:
            return knapsack_recursive(i - 1, remaining_capacity)
        else:
            return max(knapsack_recursive(i - 1, remaining_capacity),
                       values[i] + knapsack_recursive(i - 1, remaining_capacity - weights[i]))
    
    return knapsack_recursive(n - 1, capacity)

# Using functools.lru_cache
#@measure_energy(domains=[RaplPackageDomain(0)])
def knapsack_lru_cache(weights: list[int], values: list[int], capacity: int) -> int:
    n = len(weights)
    
    @lru_cache(maxsize=None)
    def knapsack_recursive(i: int, remaining_capacity: int) -> int:
        if i < 0 or remaining_capacity <= 0:
            return 0
        if weights[i] > remaining_capacity:
            return knapsack_recursive(i - 1, remaining_capacity)
        else:
            return max(knapsack_recursive(i - 1, remaining_capacity),
                       values[i] + knapsack_recursive(i - 1, remaining_capacity - weights[i]))
    
    return knapsack_recursive(n - 1, capacity)


if __name__ == '__main__':
    # Example usage
    weights = [1, 2, 3, 4]
    values = [10, 20, 30, 40]
    capacity = 5

    print("Basic Implementation:", knapsack_basic(weights, values, capacity))
    print("Using functools.cache:", knapsack_cache(weights, values, capacity))
    print("Using functools.lru_cache:", knapsack_lru_cache(weights, values, capacity))
