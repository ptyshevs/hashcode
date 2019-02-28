from parser import Photo, get_photos, Slide
from submit import submit
from tqdm import trange
import sys


def divide(photos):
    '''
    Create array of horizontal photos and vertical ones
    '''
    slides = []
    verts = []
    for p in photos:
        if p.type == 'V':
            verts.append(p)
        else:
            slides.append(Slide(p))
    return verts, slides


def concat_verts(verts: list):
    assert not len(verts) % 2
    slides = []
    with trange(len(verts), leave=True, desc="concat_verts") as pbar:
        while len(verts):
            slide = [verts.pop()]
            tags = slide[0].tags
            deleted = 1e9
            best_ind = 0
            for i, p in enumerate(verts):
                if len(tags.intersection(p.tags)) > deleted:
                    deleted = len(tags.intersection(p.tags))
                    best_ind = i
                if deleted < 5 or i > 1000:
                    break
            best_ind = 0
            slide.append(verts.pop(best_ind))
            slides.append(Slide(slide))
            pbar.update(2)
    return slides


def score_of_pair(cur, next):
    scur, snext = cur.tags, next.tags
    tags_common = scur.intersection(snext)
    tags_scur = scur - snext
    tags_snext = snext - scur
    score = min((len(tags_common), len(tags_scur), len(tags_snext)))
    return score


def concat_slides(slides: list):
    slideshow = [slides.pop()]
    with trange(len(slides), leave=True, desc="concat slides") as pbar:
        while (len(slides)):
            best_score = 0
            best_ind = 0
            # TODO count not score but lost tags
            for i, p in enumerate(slides):
                score = score_of_pair(slideshow[-1], p)
                if score > best_score:
                    best_score = score
                    best_ind = i
                if best_score > 100 or i > 2000:
                    break
            slideshow.append(slides.pop(best_ind))
            pbar.update(1)
    return slideshow


def main():
    name = sys.argv[1]
    inp = "data/" + name
    out = "dummyout/" + name
    photos = get_photos(inp)
    print(name)

    # Create array of horizontal photos and vertical ones
    verts, slides = divide(photos)

    # Create good pairs of vertical photos
    verts = sorted(verts, key=lambda s: len(s.tags), reverse=True)
    vert_slides = concat_verts(verts)

    # Add pairs of vertical photos to all slides
    slides.extend(vert_slides)

    # Sort slides
    slides = sorted(slides, key=lambda s: len(s.tags), reverse=True)

    # Concatenate photos
    slideshow = concat_slides(slides)

    # Submit
    submit(slideshow, out)


if __name__ == '__main__':
    main()
