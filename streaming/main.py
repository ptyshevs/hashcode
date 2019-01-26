from helpers import  parse, output


def main():
    input_fs = ["./input/kittens.in",
                "./input/me_at_the_zoo.in",
                "./input/submission_example.in",
                "./input/trending_today.in",
                "./input/videos_worth_spreading.in"]
    for input_f in input_fs:
        output_f = input_f.replace(".in", ".out").replace("input", "output")
        inp = parse(input_f)
        # print(slices)
        # output(output_f, )
        print('.', end='')


if __name__ == "__main__":
    main()
