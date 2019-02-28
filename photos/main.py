from parser import Photo, get_photos
from submit import submit
from tqdm import trange


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
            slides.append(p)
    return verts, slides


def concat_verts(verts: list):
    assert not len(verts) % 2
    slides = []
    with trange(len(verts)) as pbar:
        while len(verts):
            slide = [verts.pop()]
            tags = slide[0].tags
            deleted = 1e9
            best_ind = 0
            for i, p in enumerate(verts):
                if len(tags.intersection(p.tags)) > deleted:
                    deleted = len(tags.intersection(p.tags))
                    best_ind = i
            slide.append(verts.pop(best_ind))
            slides.append(slide)
            pbar.update(2)
    return slides


def score_of_pair(cur, next):
    tags_common = cur.intersection(next)
    tags_cur = cur - next
    tags_next = next - cur
    score += min((len(tags_common), len(tags_cur), len(tags_next)))
    return score


def concat_slides(slides: list):
    slideshow = [slides.pop()]
    with trange(len(slides)) as pbar:
        best_score = 0
        best_ind = 0
        # TODO count not score but lost tags
        for i, p in enumerate(slides):
            if score(slideshow[-1], p) > best_score:
                best_score = score(slideshow[-1], p)
                best_ind = i
        slideshow.append(slides.pop(best_ind))
            slide.append(verts.pop(best_ind))
            slides.append(slide)
            pbar.update(2)
    return slides


def main():
    photos = get_photos("data/e_shiny_selfies.txt")

    # Create array of horizontal photos and vertical ones
    verts, slides = divide(photos)

    # Create good pairs of vertical photos
    vert_slides = concat_verts(verts)

    # Add pairs of vertical photos to all slides
    slides.extend(vert_slides)

    slideshow = []

    # Fill slideshow
    # solve()

    # Submit
    # submit(slideshow)


if __name__ == '__main__':
    main()
