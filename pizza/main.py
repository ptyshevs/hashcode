from pasha import gen_figures, is_good_place, D2Box


def parse(input_f, p=False):
    with open(input_f, "r") as f:
        rows, cols, min_ing, max_area = map(int, f.readline().split())
        pizza = []
        for _ in range(rows):
            pizza.append(list(f.readline().replace('\n', '')))
        if p:
            print(rows, cols, min_ing, max_area)
            for i in range(rows):
                print(pizza[i])
    return rows, cols, min_ing, max_area, pizza


def output(output_f, slices):
    with open(output_f, "w") as f:
        f.write(str(len(slices)))
        f.write('\n')
        for s in slices:
            f.write(' '.join(map(str, s)))
            f.write('\n')


def put_figure(i, j, figure, pizza):
    for k in range(i, i + figure.nrow):
        for m in range(j, j + figure.ncol):
            pizza[k][m] = 'X'
    return i, j, i + figure.nrow - 1, j + figure.ncol - 1


def main():
    input_fs = ["../a_example.in",
                "../b_small.in",
                "../c_medium.in",
                "../d_big.in"]
    # input_fs = ["../d_big.in"]
    for input_f in input_fs:
        output_f = input_f.replace(".in", ".out")
        rows, cols, min_ing, max_area, pizza = parse(input_f)
        figures = gen_figures(min_ing, max_area)
        slices = []
        pasha_stop_using_classes_and_not_telling_me_about_them_GOD_DAMN_IN = D2Box(pizza)
        for i, figure in enumerate(figures[::-1]):
            print(i, "/", len(figures))
            for i in range(rows):
                for j in range(cols):
                    if is_good_place(pasha_stop_using_classes_and_not_telling_me_about_them_GOD_DAMN_IN, i, j, figure, min_ing):
                        slices.append(put_figure(i, j, figure, pizza))
        output(output_f, slices)
        print('.')


if __name__ == "__main__":
    main()
