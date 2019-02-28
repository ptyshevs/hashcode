from parser import *

def submit(slideshow, path="test.out"):
    with open(path, "w+") as f:
        print(len(slideshow), file=f)
        for slide in slideshow:
            if type(slide) == Photo:
                print(slide.id, file=f)
            else:
                print(f"{slide[0].id} {slide[1].id}", file=f)

if __name__ == '__main__':
    photos = get_photos()
    slideshow = []
    for i, pic in enumerate(photos):
        if pic.type == 'H':
            slideshow.append(pic)
        else:
            for other_pic in photos[i + 1:]:
                if other_pic.type == 'V':
                    slideshow.append([pic, other_pic])
    
    for i in slideshow:
        print(i)
    submit(slideshow)