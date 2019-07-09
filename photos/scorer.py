import sys
import os

def get_slide_tags(photos, slide):
    tags = set()
    for photo_idx in slide:
        tags.update(photos[photo_idx][2])
    return tags


def score(input_file, output_file):
    # read data
    file = open(input_file)
    n = int(file.readline().strip())
    photos = []
    for _ in range(n):
        line = file.readline().strip().split()
        photos.append([line[0], int(line[1]), set(line[2:])])

    file = open(output_file)
    n = int(file.readline().strip())
    slideshow = []
    for slide_idx in range(n):
        line = map(int, file.readline().strip().split())
        slideshow.append(line)

    total_score = 0

    p1_tags = get_slide_tags(photos, slideshow[0])
    for slide in slideshow[1:]:
        p2_tags = get_slide_tags(photos, slide)

        s1 = p1_tags & p2_tags
        s2 = p1_tags - p2_tags
        s3 = p2_tags - p1_tags

        score = min(len(s1), len(s2), len(s3))
        total_score += score

        p1_tags = p2_tags

    return total_score

if __name__ == '__main__':
    total = 0
    for filename in ["a_example.txt", "b_lovely_landscapes.txt",
                     "c_memorable_moments.txt", "d_pet_pictures.txt",
                     "e_shiny_selfies.txt"]:
        os.system(f"python3 main.py {filename}")
        s = score("data/" + filename, filename)
        print(f"{filename:.10s}: {s}")
        total += s
    print(f"Total={total}")