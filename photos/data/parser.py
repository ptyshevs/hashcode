class Photo:
    def __init__(self, id, type, tags):
        self.id = id
        self.type = type
        self.tags = tags
        self.tags[-1] = self.tags[-1][:-1]

def get_photos():
    with open("a_example.txt", "r") as data:
        number = int(data.readline()[:-1])

        photos = []
        i = 0
        while i < number :
            photo_string = data.readline()
            photo_list = photo_string.split(' ')
            photos.append(Photo(i, photo_list[0], photo_list[2:2+int(photo_list[1])]))
            i+=1
    return photos

get_photos()
