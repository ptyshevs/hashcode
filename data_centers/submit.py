from helpers import parse
import argparse
import sys


def evaluate(args):
    f_inp = args.input if args.input else "input/example.in"
    R, S, U, P, M, unavaiable, servers = parse(f_inp)
    with open(args.filename, "r") as f:
        for i in M:
            line = f.readline().split()
            if line == 'x':
                continue
            a_r, a_s, a_p = list(map(int, line.split()))
            if a_r < 0 or a_r >= R or\
                    a_s < 0 or a_s >= S or\
                    a_p < 0 or a_p >= P:
                raise RuntimeError("Wrong output at line {}".format(i))


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
