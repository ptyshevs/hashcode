from helpers import parse
import argparse
import sys


def score(R, P):
    min_cap = 1e17
    for row in range(R):
        for pool in range(P):
            capacity = 0
            for server, r in pool:
                if r != row:
                    capacity += server[1]
            if capacity < min_cap:
                min_cap = capacity
    print("BTW ur result is {}".format(min_cap))
    print("🍍")


def evaluate(args):
    f_inp = args.input if args.input else "input/example.in"
    R, S, U, P, M, unavaiable, servers = parse(f_inp)
    rows = [[False for _ in range(S)] for _ in range(R)]
    pools = [[] for _ in range(P)]
    with open(args.filename, "r") as f:
        for i in range(M):
            print("HM1")
            line = f.readline().split()
            if line == 'x':
                continue

            server = servers[i - 1]
            a_r, a_s, a_p = list(map(int, line))
            print(a_p + server[0], P)
            if a_r < 0 or a_r >= R or\
                    a_s < 0 or a_s + server[0] >= S or\
                    a_p < 0 or a_p >= P:
                __import__('ipdb').set_trace()
                raise RuntimeError("Wrong position at line {}".format(i))

            for j in range(server[0]):
                if rows[a_r][a_s + j]:
                    raise RuntimeError("Server overlaps with another "
                                       "on line {}".format(i))
                print("HM1.3")
                rows[a_r][a_s + j] = True
                print("HM1.6")
            pools[a_p].append([server, a_r])
            print("HM2")

        try:
            f.readline()
            raise RuntimeError("Too many lines")
        except:
            pass
    print("HEHEY IT DIDN'T BREAK")
    score(R, P)


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
