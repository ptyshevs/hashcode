class Photo:
    def __init__(self, id, type, tags):
        self.id = id
        self.type = type
        self.tags = tags
        self.tags[-1] = self.tags[-1][:-1]
        self.tags = set(self.tags)

    def __repr__(self):
        return f"{self.id} [{self.type}]: {self.tags}"

class Slide:
    def __init__(self, photos):
        if type(photos) == Photo:
            self.ids = [photos.id]
            self.tags = photos.tags
        else:
            self.ids = [photos[0].id, photos[1].id]
            self.tags = photos[0].tags | photos[1].tags

    def __repr__(self):
        return f"[{self.ids}, {self.tags}"


def get_photos(path="data/a_example.txt"):
    with open(path, "r") as data:
        number = int(data.readline()[:-1])

        photos = []
        i = 0
        while i < number :
            photo_string = data.readline()
            photo_list = photo_string.split(' ')
            photos.append(Photo(i, photo_list[0], photo_list[2:2+int(photo_list[1])]))
            i+=1
    return photos

def simple_slideshow(photos):
    slideshow = []
    for i, pic in enumerate(photos):
        if pic.type == 'H':
            slideshow.append(pic)
        else:
            for other_pic in photos[i + 1:]:
                if other_pic.type == 'V':
                    slideshow.append([pic, other_pic])
    return slideshow

def slide_transform(slideshow):
    # r = []
    # for slide in slideshow:
    #     if type(slide) == Photo:
    #         r.append(Slide([slide.id], [slide]))
    #     else:
    #         r.append(Slide([slide[0].id, slide[1].id], [slide[0], slide[1]]))
    return [Slide(s) for s in slideshow]

if __name__ == '__main__':
    ss = slide_transform(simple_slideshow(get_photos()))
    for _ in ss:
        print(_)
