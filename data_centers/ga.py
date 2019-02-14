import numpy as np
from Server import Server
from pruner import magic
import numpy as np
import multiprocessing
from helpers import parse
import os
import scipy

def fitness(pools, servers, M, P, R):
    least_gc = 1e17
    for i in range(P):
        gci = 1e17
        cap = sum([serv.capacity for j, serv in enumerate(servers) if pools[j] == i])
        for r in range(R):
            strike_cap = sum([serv.capacity for j, serv in enumerate(servers) if pools[j] == i and serv.row == r])
            if gci > (cap - strike_cap):
                gci = cap - strike_cap
        if gci < least_gc:
            least_gc = gci
    return least_gc

def initialize_population(population_size, M, P):
    return [np.random.randint(0, P, size=M) for _ in range(population_size)]

def score_population(population, servers, M, P, R):
    return [fitness(candidate, servers, M, P, R) for candidate in population]

def selection(population, scores, retain_frac=0.8, retain_random=0.05):
    retain_len = int(len(scores) * retain_frac)
    sorted_indices = np.argsort(scores)[::-1]
    population = [population[idx] for idx in sorted_indices]
    selected = population[:retain_len]
    leftovers = population[retain_len:]

    for gene in leftovers:
        if np.random.rand() < retain_random:
            selected.append(gene)
    return selected

def mutate(candidate, M, P, mutate_frac=0.1):
    frac = int(M * mutate_frac)
    if frac == 0:
        return
    n_tries = np.random.randint(0, int(len(candidate) * mutate_frac))

    idxs = np.random.randint(0, len(candidate), size=n_tries)
    pools = np.random.randint(0, P, size=n_tries)
    for i in range(n_tries):
        candidate[idxs[i]] = pools[i]

def crossover(mom, dad):
    select_mask = np.random.binomial(1, 0.5, size=len(mom)).astype('bool')
    child1, child2 = np.copy(mom), np.copy(dad)
    child1[select_mask] = dad[select_mask]
    child2[select_mask] = mom[select_mask]
    return child1, child2

def evolve(population, servers, M, P, R, retain_frac=0.8, retain_random=0.05, mutate_chance=0.05):
    """
    Evolution step
    :param population: list or candidate solutions
    :param target: 20x20 array that represents field in stopping condition
    :param delta: number of steps to revert
    :param retain_frac: percent of top individuals to proceed into the next genetation
    :param retain_random: chance of retaining sub-optimal individual
    :param mutate_chance: chance of mutating the particular individual
    :return: new generation of the same size
    """
    scores = score_population(population, servers, M, P, R)
    next_population = selection(population, scores, retain_frac=retain_frac, retain_random=retain_random)
    
    # mutate everyone expecting for the best candidate
    for gene in next_population[1:]:
        if np.random.random() < mutate_chance:
            mutate(gene, M, P)

    places_left = len(population) - len(next_population)
    children = []
    parent_max_idx = len(next_population) - 1
    while len(children) < places_left:
        mom_idx, dad_idx = np.random.randint(0, parent_max_idx, 2)
        if mom_idx != dad_idx:
            child1, child2 = crossover(next_population[mom_idx], next_population[dad_idx])
            children.append(child1)
            if len(children) < places_left:
                children.append(child2)
    next_population.extend(children)
    return next_population

def solve(servers, M, P, R, population_size=10, n_generations=100):
    population = initialize_population(population_size, M, P)
    for generation in range(n_generations):
        population = evolve(population, servers, M, P, R)
        if generation == 0:
            print("Generation #: best score")
        else:
            print("Generation ", generation, ": ", fitness(population[0], servers, M, P, R))
    return population[0]

def work(servers, M, P, R, n_iter):
    scipy.random.seed()
    return solve(servers, M, P, R, n_iter)

def multiprocess_solve(servers, M, P, R, n_iter=100):
    pool = multiprocessing.Pool(os.cpu_count())
    tasks = [([serv.copy() for serv in servers], M, P, R, n_iter) for _ in range(os.cpu_count())]
    results = pool.starmap(work, tasks)
    return results

def input_wrapper(inp):
    servers = []
    for i, v in enumerate(inp):
        r, slot = v[0][0], v[0][1]
        s, cap = v[1][0], v[1][1]
        serv = Server(i, s, cap)
        serv.row = r
        serv.slot = slot
        servers.append(serv)
    return servers

if __name__ == '__main__':
        path = 'input/dc.in'
        R, S, U, P, M, unavaiable, servers = parse(path)
        print("R:", R)
        print("S:", S)
        print("U:", U)
        print("P:", P)
        print("M:", M)
        # print("uavaiable:", unavaiable)
        # print("servers:", servers)
        # servers = [Server(i, _[0], _[1]) for i, _ in enumerate(servers)]
        servers = input_wrapper(magic(path))
        # example_output(servers)
        # for serv in servers:
        #     print(serv)
        res = solve(servers, M, P, R, n_generations=300)
        # for serv in servers:
        #     print(serv)