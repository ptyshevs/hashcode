import sys
import numpy as np

class Pic:
    def __init__(self, id, orient, tags):
        self.id = id
        self.orient = orient
        self.tags = tags
    
    def __repr__(self):
        return f"P[{self.id}, {self.orient}]: {self.tags}"

class Slide:
    def __init__(self, pic1, pic2=None):
        if pic2 is None:
            self.id = pic1.id
            self.tags = pic1.tags
            self.is_composed = False
        else:
            self.id = [pic1.id, pic2.id]
            self.tags_sep = [pic1.tags, pic2.tags]
            self.tags = pic1.tags | pic2.tags
            self.is_composed = True
    
    def __repr__(self):
        return f"S[{self.id}]: {self.tags}"
    

def parse_input(filename):
    pics = []
    with open(filename) as f:
        _ = int(f.readline())
        for i, line in enumerate(f):
            orient, _, *tags = line.split()
            pics.append(Pic(i, orient, set(tags)))
    return pics

class Slideshow:
    def __init__(self, seq):
        self.seq = seq
        self.scores = [connection_score(s1.tags, s2.tags) for s1, s2 in zip(seq, seq[1:])]
        self.score = sum(self.scores)
        self.n = len(seq)
    
    def __repr__(self):
        return f"Slideshow score = {self.score}"
    
    def __len__(self):
        return len(self.seq)
    
    def __getitem__(self, v):
        return self.seq[v]
    
    def __setitem__(self, k, v):
        self.seq[k] = v
    
    def swap(self, i, j):
        """ Swap two slides, accounting for change in score """
        self[i], self[j] = self[j], self[i]
        
        self.rescore(i)
        self.rescore(j)
    
    def swap_composed(self, i, j, i_k, j_m):
        """ Swap i_k pic on i-th slide with j_m pic on j slide """
        isl, jsl = self[i], self[j]
        isl.id[i_k], jsl.id[j_m] = jsl.id[j_m], isl.id[i_k]
        isl.tags_sep[i_k], jsl.tags_sep[j_m] = jsl.tags_sep[j_m], isl.tags_sep[i_k]
        isl.tags = isl.tags_sep[0] | isl.tags_sep[1]
        jsl.tags = jsl.tags_sep[0] | jsl.tags_sep[1]

        self.rescore(j)
        self.rescore(i)
    
    def rescore(self, i):
        """ Recalculate score for adjacent slides """
        if i > 0:
            prev_score = self.scores[i - 1]
            self.scores[i - 1] = connection_score(self[i - 1].tags, self[i].tags)
            self.score = self.score - prev_score + self.scores[i - 1]
        if i < self.n - 1:
            prev_score = self.scores[i]
            self.scores[i] = connection_score(self[i + 1].tags, self[i].tags)
            self.score = self.score - prev_score + self.scores[i]


def pics_to_slideshow(pics):
    """ Make a slideshow from a collection of pictures """
    collection = []
    cache = None
    for pic in pics:
        if pic.orient == "H":
            collection.append(Slide(pic))
        elif cache is None:
            cache = pic
        else:
            collection.append(Slide(pic, cache))
            cache = None
    

    return Slideshow(collection)
    

def solve(pics, n_iter=100000000, patience=50, is_slideshow=False):
    """ Using simulated annealing to optimize score """
    # horizontal_only = [Slide(pic) for pic in pics if pic.orient == "H"]

    if is_slideshow:
        sl = pics
    else:
        sl = pics_to_slideshow(pics)

    patience_cnt = 0
    for _ in range(1, n_iter + 1):
        i, j = np.random.randint(0, high=sl.n, size=(2,))
        if i != j:
            p = 0
            prev_score = sl.score
            if sl[i].is_composed and sl[j].is_composed and np.random.rand() < .5:
                i_k, j_m = np.random.randint(0, high=2, size=(2,))
                sl.swap_composed(i, j, i_k, j_m)
                mod_score = sl.score
                if mod_score < prev_score:
                    if np.random.rand() < p:
                        # print("Accepting worse modification with probability", p)
                        pass
                    else:
                        sl.swap_composed(i, j, i_k, j_m)
                        # print("Roll-back to score", sl.score)
                        patience_cnt += 1
                elif mod_score > prev_score:
                    patience_cnt = 0
            else:
                sl.swap(i, j)
                mod_score = sl.score
                if mod_score < prev_score:
                    if np.random.rand() < p:
                        print("Accepting worse modification with probability", p)
                        pass
                    else:
                        sl.swap(j, i)
                        print("Roll-back to score", sl.score)
                        patience_cnt += 1
                elif mod_score > prev_score:
                    patience_cnt = 0
                    print(f"Score improved: {sl.score}")
        if patience_cnt == patience:
            print("Early-stopping with score:", sl.score)
            break
    return sl


def eval_all():
    total = 0
    for filename in ["a_example.txt", "b_lovely_landscapes.txt",
                     "c_memorable_moments.txt", "d_pet_pictures.txt",
                     "e_shiny_selfies.txt"]:
        pics = parse_input("data/" + filename)
        slideshow = solve(pics)
        s = score(slideshow)
        print(f"{filename:.1}: {s} | slideshow = {slideshow}")
        total += s
    print(f"Total={total}")

def connection_score(ts1, ts2):
    return min(len(ts1 & ts2), len(ts1 - ts2), len(ts2 - ts1))

def score(slideshow):
    s = 0
    for i in range(len(slideshow) - 1):
        s += connection_score(slideshow[i].tags, slideshow[i+1].tags)
    return s

def submit(slideshow, out):
    with open(out, "w+") as f:
        print(len(slideshow), file=f)
        for slide in slideshow:
            id = slide.id
            if type(id) == int:
                print(id, file=f)
            else:
                print(f"{id[0]} {id[1]}", file=f)

def load_to_optimize(input_file, output_file):
    pics = parse_input(input_file)
    col = []
    with open(output_file) as f:
        f.readline()
        for i, line in enumerate(f):
            try:
                id = int(line)
                col.append(Slide(pics[id]))
            except ValueError:
                id = list(map(int, line.split()))
                col.append(Slide(pics[id[0]], pics[id[1]]))
    return Slideshow(col)



if __name__ == '__main__':
    # pics = parse_input('data/a_example.txt')
    # slideshow = [Slide(pics[0]),
    #              Slide(pics[3]),
    #              Slide(pics[1], pics[2])]
    
    # print(score(slideshow))
    
    # eval_all()

    pics = parse_input("data/b_lovely_landscapes.txt")
    slideshow = solve(pics, patience=1000000)
    submit(slideshow, "b_out.txt")

    # slideshow = load_to_optimize(sys.argv[1], sys.argv[2])
    # slideshow = solve(slideshow, patience=1e100, is_slideshow=True)
    # print(slideshow)