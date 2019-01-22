from pasha import gen_figures, is_good_place, D2Box
from helpers import output, parse, disp
# from helpers import parse, disp


def put_figure(i, j, figure, pizza):
    for k in range(i, i + figure.nrow):
        for m in range(j, j + figure.ncol):
            pizza[k][m] = 'X'
    return i, j, i + figure.nrow - 1, j + figure.ncol - 1


def convolve(inp, filt):
    rows, cols, min_ing, max_area, pizza = inp
    # Square
    assert len(filt) == len(filt[0])
    # Odd
    assert len(filt) % 2

    f_rows, f_cols = len(filt), len(filt[0])
    neighbours_sum = {}
    for i in range(rows):
        for j in range(cols):
            if pizza[i][j] == 'X':
                continue
            s = 0
            for f_i in range(f_rows):
                for f_j in range(f_cols):
                    x = i + (f_i - (f_rows - 1) // 2)
                    y = j + (f_j - (f_cols - 1) // 2)
                    v = filt[f_i][f_j]
                    item = pizza[f_i][f_j]
                    if x < 0 or y < 0 or x >= rows or y >= cols or item == 'X':
                        continue
                    s += v if item == 'M' else -v
            if abs(s) in neighbours_sum:
                neighbours_sum[abs(s)].append((i, j, s))
            else:
                neighbours_sum[abs(s)] = [(i, j, s)]
    return neighbours_sum


def cut(inp):
    rows, cols, min_ing, max_area, pizza = inp
    ksize = 3
    filt = [[10 - (abs(x) + abs(y)) for x in range(-ksize, ksize + 1)]
            for y in range(-ksize, ksize + 1)]
    filt[ksize][ksize] = 0
    slices = []
    figures = gen_figures(min_ing, max_area)
    potato = D2Box(pizza)
    prev_key = None
    # disp(pizza)
    while True:
        inp = rows, cols, min_ing, max_area, pizza
        neighbours_sum = convolve(inp, filt)
        # print(neighbours_sum)
        if prev_key is not None and prev_key in neighbours_sum:
            for item in neighbours_sum[prev_key]:
                x, y, v = item
                pizza[x][y] = 'X'
        if len(neighbours_sum) == 0:
            break
        key = max(neighbours_sum.keys())
        prev_key = key
        for item in neighbours_sum[key]:
            # print()
            # print()
            # disp(pizza)
            x, y, v = item
            # print()
            # print()
            # print(x, y, v)
            # print()
            best = None
            item = pizza[x][y]
            if item == 'X':
                continue
            for figure in figures:
                for offset_x in range(-(figure.nrow - 1), 1):
                    for offset_y in range(-(figure.ncol - 1), 1):
                        o_x, o_y = x + offset_x, y + offset_y
                        score = is_good_place(potato, o_x, o_y, figure, min_ing)
                        ind = 0 if key > 10 else 1
                        # print(o_x, o_y, score)
                        # print(figure)
                        # print()
                        if score is False:
                            continue
                        elif best is None:
                            best = o_x, o_y, figure, score[ind]
                        elif item == 'M' and score[ind] > best[3]:
                            best = o_x, o_y, figure, score[ind]
                        elif item == 'T' and score[ind] < best[3]:
                            best = o_x, o_y, figure, score[ind]
            if best is not None:
                slices.append(put_figure(*best[:3], pizza))
            # disp(pizza)
    return slices


def main():
    input_fs = [#"input/a_example.in",
    # "input/b_small.in",]
    "input/c_medium.in",
    "input/d_big.in"]
    # input_fs = ["input/b_small.in",]
    for input_f in input_fs:
        output_f = input_f.replace(".in", ".out").replace("input", "output")
        inp = parse(input_f)
        rows, cols, min_ing, max_area, pizza = inp
        slices = cut(inp)
        # print(slices)
        output(output_f, slices)
        print('.')


if __name__ == "__main__":
    main()
