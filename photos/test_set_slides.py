from set_photos import Slide, get_slides
from ga import solve
from submit import submit

if __name__ == '__main__':
    slides = get_slides('data/d_pet_pictures.txt')
    print(len(slides))
    res = solve(slides, len(slides), 20, 2000)
    new_slides = [slides[i] for i in res]
    submit(new_slides, "test_slides.out")
