import sys


def parse(filename="input/dc.in"):
    """Parses the input

    :filename: path to the input file
    :returns:
        R(1 ≤ R ≤ 1000) denotes the number of rows in the data center,
        S(1 ≤ S ≤ 1000) denotes the number of slots in each row of the data
            center,
        U(0 ≤ U ≤ R × S) denotes the number of unavailable slots,
        P(1 ≤ P ≤ 1000) denotes the number of pools to be created,
        M(1 ≤ M ≤ R × S) denotes the number of servers to be allocated;
        U subsequent lines describing the unavailable slots of the data center.
            Each of these lines contains two natural numbers separated by a
            single space: ri and si, denoting the row number (ri) and the slot
            number within the row (si) of the particular unavailable slot;
        M subsequent lines describing the servers to be allocated. Each of these
            lines contains two natural numbers separated by a single space: zi
            and ci (1 ≤ z , 000) , denoting the size i ≤ S 1 ≤ c i ≤ 1 of the
            server (zi), ie. the number of slots that it occupies, and the
            capacity (ci) of the machine.

    """
    try:
        with open(filename, "r") as f:
            R, S, U, P, M = list(map(int, f.readline().split()))
            unavaiable = []
            servers = []
            for _ in range(U):
                unavaiable.append(list(map(int, f.readline().split())))
            for _ in range(M):
                servers.append(list(map(int, f.readline().split())))
    except IOError as e:
        print(e)
        sys.exit(1)
    return R, S, U, P, M, unavaiable, servers
