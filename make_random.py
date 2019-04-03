import sys
import os
from random import randint
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


def calc_paste_params(canvas_width, canvas_height):
    MAX_ANGLE = 20
    MAX_COMPRESSION_RATE = 10

    x = randint(0, canvas_width)
    y = randint(0, canvas_height)
    angle = randint(-1 * MAX_ANGLE, MAX_ANGLE)
    rate = randint(1, MAX_COMPRESSION_RATE)
    return x, y, angle, rate


def compress_with_rate(im, rate):
    return im.resize((int(im.width / rate), int(im.height / rate)))


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
    MAX_PASTE_NUM = 200

    ims, imwidths, imheights = get_im_data(FILEDIR)
    canvas = Image.new(
        'RGB', (canvas_width, canvas_height), (0, 0, 0))

    paste_count = 0
    paste_ratio = 0
    while (paste_ratio < MIN_PASTE_RATIO) and (paste_count < MAX_PASTE_NUM):
        # paste
        for i in range(len(ims)):
            x, y, angle, rate = calc_paste_params(canvas_width, canvas_height)
            canvas.paste(
                compress_with_rate(ims[i], rate).rotate(angle),
                (x, y))
        paste_count += 1
        paste_ratio = calc_paste_ratio(canvas)

    print('[DEBUG] PASTE COUNT: %s' % paste_count)
    print('[DEBUG] PASTE RATIO: %s' % paste_ratio)
    canvas.save('%s.jpg' % output_filename, quality=100)
