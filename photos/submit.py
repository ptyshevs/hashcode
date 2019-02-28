def submit(slideshow, path="test.out"):
    with open(path, "w+") as f:
        print(len(slideshow), file=f)
        for slide in slideshow:
            if type(slide) == Photo:
                print(slide.id, file=f)
            else:
                print(f"{slide[0].id} {slide[1].id}", file=f)
