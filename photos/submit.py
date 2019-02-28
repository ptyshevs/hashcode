from parser import Photo

def submit(slideshow, path="test.out"):
    with open(path, "w+") as f:
        print(len(slideshow), file=f)
        for slide in slideshow:
            print(" ".join([str(id) for id in slide.ids]), file=f)
