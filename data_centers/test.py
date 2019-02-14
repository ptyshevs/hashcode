from helpers import parse


def main():
    R, S, U, P, M, unavaiable, servers = parse("input/example.in")
    print(R, S, U, P, M)
    for u in unavaiable:
        print(u)
    for s in servers:
        print(s)


if __name__ == "__main__":
    main()
