from parser import *


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