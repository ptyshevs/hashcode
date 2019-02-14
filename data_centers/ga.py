from helpers import parse
from Server import Server
import numpy as np

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

def mutate(candidate, M, P):
    pass

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
        R, S, U, P, M, unavaiable, servers = parse('input/example.in')
        print("R:", R)
        print("S:", S)
        print("U:", U)
        print("P:", P)
        print("M:", M)
        print("uavaiable:", unavaiable)
        print("servers:", servers)
        servers = [Server(i, _[0], _[1]) for i, _ in enumerate(servers)]
        example_output(servers)
        for serv in servers:
            print(serv)