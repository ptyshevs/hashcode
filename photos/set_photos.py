import parser
from operator import attrgetter

class Slide:
    def __init__(self, photo1, photo2=0):
        if photo2 != 0:
            self.ids = [photo1.id,  photo2.id]
            self.tags = photo1.tags & photo2.tags
        else:
            self.ids = [photo1.id]
            self.tags = photo1.tags
        self.tags_len = len(self.tags)

def get_slides(path):
    photos = parser.get_photos(path)
    slides = []
    all_posibilities = [[Slide(x1, x2), len(x1.tags & x2.tags)] for x1 in photos for x2 in photos if x1.type == 'V' and x2.type == 'V' and x1 != x2]
    for x1 in photos:
        x1_containers = [x for x in all_posibilities if x[0].ids[0] == x1.id]
        if len(x1_containers) > 0:
            slides.append(max(x1_containers, key=lambda x: x[1])[0])
            all_posibilities = [x for x in all_posibilities if x[0].ids[0] != x1.id and x[0].ids[1] != x1.id]
    for x1 in photos:
        if x1.type == 'H':
            slides.append(x1)
    return slides
