from helpers import parse
from Server import Server
from pruner import magic
import numpy as np
import multiprocessing
import os
import scipy

def is_allocated(serv):
    return serv.row != -1 and serv.slot != -1

def score(R, P):
    min_cap = 1e17
    for row in range(R):
        for pool in range(P):
            capacity = 0
            for server, r in pool:
                if r != row:
                    capacity += server.capacity
            if capacity < min_cap:
                min_cap = capacity
    print(min_cap)
    return min_cap

def my_score(candidate, M, P, R):
    pool_gcs = []
    for i in range(P):
        gci = 1e17
        cap = sum([serv.capacity for serv in candidate if serv.pool == i])
        # print("Total cap:", cap)
        for r in range(R):
            strike_cap = sum([serv.capacity for serv in candidate if serv.pool == i and serv.row == r])
            if (cap - strike_cap) < 0:
                print("Somethin' vent wrong: capacity {} is smaller then strike capacity {}".format(cap, strike_cap))
            elif gci > (cap - strike_cap):
                gci = cap - strike_cap
        pool_gcs.append(gci)
    # print(pool_gcs)
    return min(pool_gcs)

def mutate(M, P):
    n_tries = np.random.randint(0, 20)

    idxs = np.random.randint(0, M, size=n_tries)
    pools = np.random.randint(0, P, size=n_tries)
    return idxs, pools

def solve_step(candidate, M, P, R, accept_prob=0.5, prev_score=0):
    idxs, pools = mutate(len(candidate), P)
    # print("chose:", candidate[serv_idx])
    prev_pools = [candidate[serv_idx].pool for serv_idx in idxs]
    for i, serv_idx in enumerate(idxs):
        candidate[serv_idx].pool = pools[i]
    candidate_score = my_score(candidate, M, P, R)
    if candidate_score > prev_score:
        if np.random.random() < accept_prob:
            return candidate_score, True
        else:
            for i, serv_idx in enumerate(idxs):
                candidate[serv_idx].pool = prev_pools[i]
            return prev_score, False
    else:
        return prev_score, False

def solve(servers, M, P, R, n_iter=100):
    accept_prob = 0.9
    best_score = 0
    cnt = 1
    for i in range(n_iter):
        score, changed = solve_step(servers, M, P, R, accept_prob, best_score)
        if score > best_score:
            best_score = score
            accept_prob =  np.exp(-0.01 * cnt)
            cnt += 1
        if i > 0 and i % 50 == 0:
            print("{}: {} - changed {} | best score: {} | accept_prob: {}".format(i, score, changed, best_score, accept_prob))
    return servers, best_score

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

def example_output(servers):
    servers[0].row = 0
    servers[0].slot = 1
    servers[0].pool = 0

    servers[1].row = 1
    servers[1].slot = 0
    servers[1].pool = 1

    servers[2].row = 1
    servers[2].slot = 3
    servers[2].pool = 0

    servers[3].row = 0
    servers[3].slot = 4
    servers[3].pool = 1

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
        best_of_the_best_of_the_best = [[], 0]
        for reinit in range(10):
            print("initialization #", reinit)
            result = multiprocess_solve(servers, len(servers), P, R, 1000)
            best_of_the_best = max(result, key=lambda x:x[1])
            if best_of_the_best[1] > best_of_the_best_of_the_best[1]:
                best_of_the_best_of_the_best[0] = [_.copy() for _ in best_of_the_best[0]]
                best_of_the_best_of_the_best[1] = best_of_the_best[1]
            print("Best of the best score for iteration {}: {}".format(reinit, best_of_the_best[1]))
        print("Best of the best of the best score:", best_of_the_best_of_the_best[1])
        # for serv in servers:
        #     print(serv)