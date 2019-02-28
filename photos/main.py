from parser import *
from submit import *



if __name__ == '__main__':
    photos = get_photos()

    
    for i in slideshow:
        print(i)
    
    submit(slideshow)