import numpy as np
from parser import *
import numpy as np
import multiprocessing
import os
import scipy
from submit import submit

def fitness(ids, slideshow):
    score = 0
    for cur, next in zip(ids, ids[1:]):
        scur, snext = set(slideshow[cur].tags), set(slideshow[next].tags)
        tags_common = scur.intersection(snext)
        tags_cur = scur - snext
        tags_next = snext - scur
        score += min((len(tags_common), len(tags_cur), len(tags_next)))
    return score

def initialize_population(population_size, N):
    return [np.random.permutation(list(range(N))) for _ in range(population_size)]

def score_population(population, slideshow):
    return [fitness(candidate, slideshow) for candidate in population]

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

def mutate(candidate, mutate_frac=0.1):
    n_swaps = int(len(candidate) * mutate_frac)
    for i in range(n_swaps):
        i_f, i_t = np.random.randint(0, len(candidate), size=2)
        candidate[i_f], candidate[i_t] = candidate[i_t], candidate[i_f]

def crossover(mom, dad):
    select_mask = np.random.binomial(1, 0.5, size=len(mom)).astype('bool')
    child1, child2 = np.copy(mom), np.copy(dad)
    child1[select_mask] = dad[select_mask]
    child2[select_mask] = mom[select_mask]
    return child1, child2

def evolve(population, slideshow, retain_frac=0.8, retain_random=0.05, mutate_chance=0.05):
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
    scores = score_population(population, slideshow)
    next_population = selection(population, scores, retain_frac=retain_frac, retain_random=retain_random)
    
    # mutate everyone expecting for the best candidate
    for gene in next_population[1:]:
        if np.random.random() < mutate_chance:
            mutate(gene)

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

def solve(slideshow, N, population_size=10, n_generations=100):
    population = initialize_population(population_size, N)
    print(population)
    for generation in range(n_generations):
        population = evolve(population, slideshow)
        if generation == 0:
            print("Generation #: best score")
        else:
            print("Generation ", generation, ": ", fitness(population[0], slideshow))
    return population[0]

def work(servers, M, P, R, n_iter):
    scipy.random.seed()
    return solve(servers, M, P, R, n_iter)

def multiprocess_solve(servers, M, P, R, n_iter=100):
    pool = multiprocessing.Pool(os.cpu_count())
    tasks = [([serv.copy() for serv in servers], M, P, R, n_iter) for _ in range(os.cpu_count())]
    results = pool.starmap(work, tasks)
    return results


def solve_all():
    for fname in ["data/a_example.txt",
                  "data/b_lovely_land"]

if __name__ == '__main__':
    path = 'data/d_pet_pictures.txt'
    photos = get_photos(path)
    slideshow = slide_transform(simple_slideshow(photos))
    res = solve(slideshow, len(slideshow), 10, 30)
    new_slideshow = [slideshow[i] for i in res]
    submit(new_slideshow, path[:-3] + 'out')