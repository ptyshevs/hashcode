import sys


class D2Box:
    def __init__(self, box):
        self.box = box
        self.nrow = len(box)
        self.ncol = len(box[0])


class Figure:
    def __init__(self, nrow, ncol):
        self.nrow = nrow
        self.ncol = ncol

    def __repr__(self):
        return '\n'.join(['*' * self.ncol for i in range(self.nrow)])


def is_good_place(map: D2Box, i, j, figure: Figure, L):
    """
    figure is assumed to have area in range [2L, H]
    """
    cnt_tomato, cnt_mushroom = 0, 0

    if i + figure.nrow > map.nrow or j + figure.ncol > map.ncol or\
            i < 0 or j < 0:
        return False

    # iterating by figure
    for k in range(figure.nrow):
        for m in range(figure.ncol):
            coord = map.box[i + k][j + m]
            if coord == 'T':
                cnt_tomato += 1
            elif coord == 'M':
                cnt_mushroom += 1
            elif coord == 'X':  # This place is occupied by another figure
                return False
    if cnt_tomato >= L and cnt_mushroom >= L:
        return (cnt_mushroom - cnt_tomato, figure.nrow * figure.ncol)
    else:
        return False


def divisors(n):
    return {x for x in range(2, (n + 1) // 2 + 1) if n % x == 0 and n != x}


def gen_figures(L, H):
    min_area = 2 * L
    max_area = H
    lst = []
    # area = 4
    for area in range(max_area, min_area - 1, -1):
        nrows = divisors(area)
        lst.append(Figure(1, area))
        for nrow in nrows:
            lst.append(Figure(nrow, (area // nrow)))
        lst.append(Figure(area, 1))
    return lst


if __name__ == '__main__':
    if len(sys.argv) > 1:
        fname = sys.argv[1]
    else:
        exit()
    with open(fname) as f:
        n_rows, n_cols, L, H = list(map(int, f.readline().split()))
        M = [f.readline().rstrip('\n') for _ in range(n_rows)]
    M = D2Box(M)
    figure = Figure(1, 2)

    print(is_good_place(M, 2, 0, figure, L))
    for fig in gen_figures(L, H):
        print(fig)
        print("")
