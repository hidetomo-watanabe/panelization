import sys
import os
import random
from PIL import Image


def get_im_data(FILEDIR):
    ims = []
    imwidths = []
    imheights = []
    for filename in os.listdir(FILEDIR):
        if filename == '.gitkeep':
            continue
        im = Image.open('%s/%s' % (FILEDIR, filename))
        ims.append(im)
        imwidths.append(im.size[0])
        imheights.append(im.size[1])
    return ims, imwidths, imheights


def get_random_params(CANVAS_WIDTH, CANVAS_HEIGHT):
    # const
    RANDOM_BUFFER_RATIO = 0.8
    ROTATE_MAX = 20

    width_random = random.randint(
        0, CANVAS_WIDTH * RANDOM_BUFFER_RATIO)
    height_random = random.randint(
        0, CANVAS_HEIGHT * RANDOM_BUFFER_RATIO)
    rotate_random = random.randint(-1 * ROTATE_MAX, ROTATE_MAX)
    return width_random, height_random, rotate_random


if __name__ == '__main__':
    if len(sys.argv) > 1:
        output_filename = sys.argv[1]
    else:
        output_filename = 'tmp'
    if len(sys.argv) > 2:
        paste_num = int(sys.argv[2])
    else:
        paste_num = 1

    # const
    FILEDIR = './files'
    CANVAS_WIDTH = 1440
    CANVAS_HEIGHT = 900

    ims, imwidths, imheights = get_im_data(FILEDIR)
    canvas = Image.new(
        'RGB', (CANVAS_WIDTH, CANVAS_HEIGHT), (0, 0, 0))
    for _ in range(paste_num):
        for i in range(len(ims)):
            width_random, height_random, rotate_random = \
                get_random_params(CANVAS_WIDTH, CANVAS_HEIGHT)
            canvas.paste(
                ims[i].rotate(rotate_random),
                (width_random, height_random))

    canvas.save('%s.jpg' % output_filename, quality=100)
