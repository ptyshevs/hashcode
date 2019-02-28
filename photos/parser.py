class Photo:
    def __init__(self, id, type, tags):
        self.id = id
        self.type = type
        self.tags = tags
        self.tags[-1] = self.tags[-1][:-1]
        self.tags = set(self.tags)

    def __repr__(self):
        return f"{self.id} [{self.type}]: {self.tags}"

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
