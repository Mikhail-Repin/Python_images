import matplotlib.pyplot as plt
from imageio.v2 import imread
from imageio.v2 import imwrite
from transformations import reduce, make_transform, bright
import numpy as np
import math


def all_transform(img, dsize, rsize, step):
    factor = dsize // rsize
    transformed_blocks = []
    for i in range((img.shape[0] - dsize) // step + 1):
        for j in range((img.shape[1] - dsize) // step + 1):
            cp_block = reduce(img[i*step:i*step+dsize, j*step:j*step+dsize], factor)
            for val, angle in candidates:
                transformed_blocks.append((i, j, val, angle, make_transform(cp_block, val, angle)))
    return transformed_blocks


def compress(img, dsize, rsize, step):
    com_array = []
    transformed_blocks = all_transform(img,dsize, rsize, step)
    i_count = img.shape[0] // rsize
    j_count = img.shape[1] // rsize
    f = open('res.bin', 'wb')
    f.write((str(i_count) + '\n').encode())
    f.write((str(j_count) + '\n').encode())
    for i in range(i_count):
        com_array.append([])
        for j in range(j_count):
            print("{}/{} ; {}/{}".format(i, i_count, j, j_count))
            com_array[i].append(None)
            min_d = float('inf')
            R = img[i*rsize:(i+1)*rsize,j*rsize:(j+1)*rsize]
            for k, l, val, angle, D in transformed_blocks:
                contrast, brightness = bright(R, D)
                D = contrast*D + brightness
                d = np.sum(np.square(R - D))
                if d < min_d:
                    min_d = d
                    com_array[i][j] = (k, l, val, angle, contrast, brightness)
            for t in range(len(com_array[i][j])):
                if t != len(com_array[i][j])-1:
                    f.write((str(com_array[i][j][t])).encode())
                else:
                    f.write((str(com_array[i][j][t])+'\n').encode())
    f.close()
    return com_array


def decompress(com_array, dsize, rsize, step, nb_iter=10):
    factor = dsize // rsize
    height = len(com_array) * rsize
    width = len(com_array[0]) * rsize
    iterations = [np.full((height, width), 1)]
    cur_img = np.zeros((height, width))
    for i_iter in range(nb_iter):
        print(i_iter)
        for i in range(len(com_array)):
            for j in range(len(com_array[i])):
                k, l, flip, angle, contrast, brightness = com_array[i][j]
                D = reduce(iterations[-1][k*step:k*step+dsize, l*step:l*step+dsize], factor)
                #print(D.shape[0], D.shape[1])
                R = make_transform(D, flip, angle, contrast, brightness)
                cur_img[i*rsize:(i+1)*rsize, j*rsize:(j+1)*rsize] = R
        iterations.append(cur_img)
        cur_img = np.zeros((height, width))
    return iterations


def result(iterations, ideal = None):
    plt.figure()
    nb_row = math.ceil(np.sqrt(len(iterations)))
    nb_cols = nb_row
    for i, img in enumerate(iterations):
        plt.subplot(nb_row, nb_cols, i+1)
        plt.imshow(img, cmap='gray', vmin=0, vmax=255, interpolation='none')
        if ideal.shape[0] == img.shape[0] and ideal.shape[1] == img.shape[1]:
            plt.title(str(i) + ' (' + '{0:.2f}'.format(np.sqrt(np.mean(np.square(ideal - img)))) + ')')
            out = str(i) + ' (' + '{0:.2f}'.format(np.sqrt(np.mean(np.square(ideal - img)))) + ')' + '.jpg'
        else:
            plt.title(str(i))
            out = str(i) + '.jpg'
        img_uint8 = img.astype(np.uint8)
        imwrite(out, img_uint8, format='jpg')
        frame = plt.gca()
        frame.axes.get_xaxis().set_visible(False)
        frame.axes.get_yaxis().set_visible(False)
    plt.tight_layout()


reflects = [1, -1]
angles = [0, 90, 180, 270]
candidates = [[val, angle] for val in reflects for angle in angles]


def make_gray(img):
    return np.mean(img[:, :, :2], 2)


if __name__ == '__main__':
    img = imread('lena.bmp')
    img = make_gray(img)
    img = reduce(img, 8)
    side = min(img.shape[0], img.shape[1])
    com_array = compress(img[:side, :side], 8, 4, 4)
    iterations = decompress(com_array, 8, 4, 4)
    result(iterations, img)
    plt.show()
