import sys
import os
import random
from PIL import Image


def get_im_data(filedir):
    ims = []
    imwidths = []
    imheights = []
    for filename in os.listdir(filedir):
        if filename == '.gitkeep':
            continue
        im = Image.open('%s/%s' % (filedir, filename))
        ims.append(im)
        imwidths.append(im.size[0])
        imheights.append(im.size[1])
    return ims, imwidths, imheights


def get_random_params(canvas_width, canvas_height):
    # const
    RANDOM_BUFFER_RATIO = 0.8
    ROTATE_MAX = 20

    width_random = random.randint(
        0, canvas_width * RANDOM_BUFFER_RATIO)
    height_random = random.randint(
        0, canvas_height * RANDOM_BUFFER_RATIO)
    rotate_random = random.randint(-1 * ROTATE_MAX, ROTATE_MAX)
    return width_random, height_random, rotate_random


def calc_paste_ratio(canvas):
    zero_count = 0
    non_zero_count = 0
    for count, pixel in canvas.getcolors(256**3):
        if sum(pixel) == 0:
            zero_count += count
        else:
            non_zero_count += count
    paste_ratio = non_zero_count / (non_zero_count + zero_count)
    return paste_ratio


if __name__ == '__main__':
    if len(sys.argv) > 1:
        output_filename = sys.argv[1]
    else:
        output_filename = 'tmp'
    if len(sys.argv) > 2:
        canvas_width = sys.argv[2]
    else:
        canvas_width = 1440
    if len(sys.argv) > 3:
        canvas_width = sys.argv[3]
    else:
        canvas_height = 900

    # const
    FILEDIR = './files'
    MIN_PASTE_RATIO = 0.7
    MAX_PASTE_NUM = 100

    ims, imwidths, imheights = get_im_data(FILEDIR)
    canvas = Image.new(
        'RGB', (canvas_width, canvas_height), (0, 0, 0))

    paste_count = 0
    paste_ratio = 0
    while (paste_ratio < MIN_PASTE_RATIO) and (paste_count < MAX_PASTE_NUM):
        # paste
        for i in range(len(ims)):
            width_random, height_random, rotate_random = \
                get_random_params(canvas_width, canvas_height)
            canvas.paste(
                ims[i].rotate(rotate_random),
                (width_random, height_random))
        paste_count += 1
        paste_ratio = calc_paste_ratio(canvas)

    print('[DEBUG] PASTE COUNT: %s' % paste_count)
    print('[DEBUG] PASTE RATIO: %s' % paste_ratio)
    canvas.save('%s.jpg' % output_filename, quality=100)
