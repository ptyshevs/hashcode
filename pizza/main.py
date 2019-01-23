from pasha import gen_figures, is_good_place, D2Box
from helpers import output, parse, disp


def put_figure(x, y, figure, pizza):
    for k in range(x, x + figure.nrow):
        for m in range(y, y + figure.ncol):
            pizza[k][m] = 'X'
    return x, y, x + figure.nrow - 1, y + figure.ncol - 1


def convolution(inp, filt, neighbours_sum, x, y):
    rows, cols, min_ing, max_area, pizza = inp
    if pizza[x][y] == 'X':
        continue
    f_rows, f_cols = len(filt), len(filt[0])
    s = 0

    for x_offs in range((f_rows - 1) // 2, (f_rows - 1) // 2 + 1):
        for y_offs in range((f_cols - 1) // 2, (f_cols - 1) // 2 + 1):
            x_shif = x + x_offs
            y_shif = y + y_offs
            v = filt[x_offs][y_offs]
            if x_shif < 0 or y_shif < 0 or x_shif >= rows or\
                    y_shif >= cols or pizza[x_shif][y_shif] == 'X':
                continue
            s += v if pizza[x_shif][y_shif] == 'M' else -v

    if abs(s) in neighbours_sum:
        neighbours_sum[abs(s)].append((x, y, s))
    else:
        neighbours_sum[abs(s)] = [(x, y, s)]


def convolve(inp, filt):
    rows, cols, min_ing, max_area, pizza = inp
    assert len(filt) == len(filt[0])
    assert len(filt) % 2

    neighbours_sum = {}

    for x in range(rows):
        for y in range(cols):
            convolution(inp, filt, neighbours_sum, x, y)
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
            x, y, v = item
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
    return slices


def main():
    input_fs = ["input/a_example.in",
                "input/b_small.in",
                "input/c_medium.in",
                "input/d_big.in"]
    for input_f in input_fs:
        output_f = input_f.replace(".in", ".out").replace("input", "output")
        inp = parse(input_f)
        rows, cols, min_ing, max_area, pizza = inp
        slices = cut(inp)
        # print(slices)
        output(output_f, slices)
        print('.', end='')


if __name__ == "__main__":
    main()
