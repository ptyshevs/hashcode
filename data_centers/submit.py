from helpers import parse
import argparse
import sys
from tqdm import trange, tqdm


def score(R, pools):
    min_cap = 1e17
    for row in trange(R, desc="Calculating the score", leave=False):
        for pool in pools:
            capacity = 0
            for server, r in pool:
                if r != row:
                    capacity += server[1]
            if capacity < min_cap:
                min_cap = capacity
    print("BTW ur result is {}".format(min_cap))
    print("🍍")


def evaluate(args):
    f_inp = args.input if args.input else "input/dc.in"
    print("FILE:", f_inp)
    R, S, U, P, M, unavaiable, servers = parse(f_inp)
    rows = [[False for _ in range(S)] for _ in range(R)]
    pools = [[] for _ in range(P)]
    with open(args.filename, "r") as f:
        for i in trange(M, desc="Parsing the file", leave=False):
            line = f.readline().split()
            if line[0] == 'x' and len(line) == 1:
                continue

            server = servers[i]
            a_r, a_s, a_p = list(map(int, line))
            print("R:", R)
            if a_r < 0 or a_r >= R:
                print("ROW PROBLEM")
                raise RuntimeError("Wrong position at line {}: pool {}, row {}, slot {}".format(i, a_p, a_r, a_s))
            elif a_s < 0 or a_s + server[0] - 1 >= S:
                print("SLOT PROB")
                raise RuntimeError("Wrong position at line {}: pool {}, row {}, slot {}".format(i, a_p, a_r, a_s))
            elif a_p < 0 or a_p >= P:
                print("POOL")
                raise RuntimeError("Wrong position at line {}: pool {}, row {}, slot {}".format(i, a_p, a_r, a_s))
            for j in range(server[0]):
                if rows[a_r][a_s + j]:
                    raise RuntimeError("Server overlaps with another "
                                       "on line {}".format(i))
                rows[a_r][a_s + j] = True
            pools[a_p].append([server, a_r])

        try:
            f.readline()
            raise RuntimeError("Too many lines")
        except:
            pass
    print("HEHEY IT DIDN'T BREAK")
    score(R, pools)


def pargs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", default=None, required=True,
                        help="Path to the solution")
    parser.add_argument("-i", "--input", default=None, help="Path to the input")
    return parser.parse_args()


def main():
    args = pargs()
    try:
        evaluate(args)
    except Exception as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
