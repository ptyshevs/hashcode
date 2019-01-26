from helpers import  parse, output


class CacheServer:
    def __init__(self, id, capacity):
        self.id = id
        self.capacity = capacity
        self.capacity_used = 0
        self.videos_id = []

    def __repr__(self):
        return f"C{self.id} [{self.capacity_used}/{self.capacity}]: {self.videos_id}"


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
    # main()
    n_vid, n_endp, n_req, n_ser, cap_ser, vid_sizes, endps, reqs = parse('input/submission_example.in')
    cs_vid_pairs = dict()
    for req in reqs:
        v_id, e_id, n = req
        
        endpoint = endps[e_id]
        for cs_id, cs_latency in endpoint.caches_connections.items():
            dc_latency = endpoint.latency
            profit = (dc_latency - cs_latency)
            print(f"Profit for storing V{v_id} on C{cs_id} is {profit}")
            if (v_id, cs_id) not in cs_vid_pairs:
                cs_vid_pairs[(v_id, cs_id)] = profit
            else:
                cs_vid_pairs[(v_id, cs_id)] += profit
    sorted_by_profit = sorted(cs_vid_pairs, key=cs_vid_pairs.get, reverse=True)

    cs_by_vid = [CacheServer(_, cap_ser) for _ in range(n_ser)]  # list of lists
    for (v_id, cs_id) in sorted_by_profit:
        cs = cs_by_vid[cs_id]
        v_size = vid_sizes[v_id]
        if cs.capacity_used + v_size < cs.capacity:
            cs.capacity_used += v_size
            cs.videos_id.append(v_id)

    with open('test.out', 'w+') as f:
        print(len(cs_by_vid), file=f)
        for i in range(len(cs_by_vid)):
            cs = cs_by_vid[i]
            print(f"{str(i)} {' '.join([str(_) for _ in cs.videos_id])}", file=f)
    print("cs_by_vid:", cs_by_vid)
