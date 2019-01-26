from helpers import  parse, output
import tqdm

class CacheServer:
    def __init__(self, id, capacity):
        self.id = id
        self.capacity = capacity
        self.capacity_used = 0
        self.videos_id = []

    def __repr__(self):
        return f"C{self.id} [{self.capacity_used}/{self.capacity}]: {self.videos_id}"


def solve(inp):
    n_vid, n_endp, n_req, n_ser, cap_ser, vid_sizes, endps, reqs = inp
    cs_vid_pairs = dict()
    # print(endps)
    for req in reqs:
        v_id, e_id, n = req
        
        endpoint = endps[e_id]
        for cs_id, cs_latency in endpoint.caches_connections.items():
            dc_latency = endpoint.latency
            profit = (dc_latency - cs_latency) * n
            # print(f"Profit for storing V{v_id} on C{cs_id} is {profit}")
            if (v_id, cs_id) not in cs_vid_pairs:
                cs_vid_pairs[(v_id, cs_id)] = profit
            else:
                cs_vid_pairs[(v_id, cs_id)] += profit
    sorted_by_profit = sorted(cs_vid_pairs, key=cs_vid_pairs.get, reverse=True)
    # print("sorted by profit:", sorted_by_profit)
    cs_by_vid = [CacheServer(_, cap_ser) for _ in range(n_ser)]  # list of lists
    for (v_id, cs_id) in sorted_by_profit:
        cs = cs_by_vid[cs_id]
        v_size = vid_sizes[v_id]
        if cs.capacity_used + v_size < cs.capacity:
            cs.capacity_used += v_size
            cs.videos_id.append(v_id)
    return cs_by_vid


def main():
    input_fs = [
                "./input/0_submission_example.in",
                "./input/1_me_at_the_zoo.in",
                "./input/2_videos_worth_spreading.in",
                "./input/3_trending_today.in",
                "./input/4_kittens.in",]
    for input_f in tqdm.tqdm(input_fs):
        output_f = input_f.replace(".in", ".out").replace("input", "output")
        inp = parse(input_f)
        cs_by_vid = solve(inp)
        output(output_f, cs_by_vid)
        # break
        print('.', end='')


if __name__ == "__main__":
    main()
