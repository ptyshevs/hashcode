class Endpoint:
    def __init__(self, endp_id, dc_latency, caches_connections):
        self.id = endp_id
        self.latency = dc_latency  # latency for requesting video directly from datacenter
        self.caches_connections = caches_connections

    def __repr__(self):
        return f"E{self.id}: {self.latency}, {self.caches_connections}"


def parse(input_f):
    with open(input_f, "r") as f:
        n_vid, n_endp, n_req, n_ser, cap_ser = map(int, f.readline().split())
        vid_sizes = []
        endps = []
        reqs = []
        vid_sizes = list(map(int, f.readline().split()))
        for endpoint_id in range(n_endp):
            dc_latency, n_caches = list(map(int, f.readline().split()))
            caches_connections = {}
            for cache in range(n_caches):
                cs_id, cs_latency = list(map(int, f.readline().split()))
                caches_connections[cs_id] = cs_latency
            endps.append(Endpoint(endpoint_id, dc_latency, caches_connections))
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
