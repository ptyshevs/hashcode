def parse(input_f):
    with open(input_f, "r") as f:
        n_vid, n_endp, n_req, n_ser, cap_ser = map(int, f.readline().split())
        vid_sizes = []
        endps = []
        reqs = []
        for _ in range(n_vid):
            vid_sizes.append(list(map(int, f.readline().split())))
        for _ in range(n_endp):
            endps.append(list(map(int, f.readline().split())))
        for _ in range(n_req):
            reqs.append(list(map(int, f.readline().split())))
    return n_vid, n_endp, n_req, n_ser, cap_ser, vid_sizes, endps, reqs


def output(output_f, caches):
    with open(output_f, "w") as f:
        f.write(str(len(caches)))
        f.write('\n')
        for i, s in enumerate(caches):
            f.write(' '.join(map(str, [i] + s)))
            f.write('\n')
