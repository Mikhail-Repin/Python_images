from numpy import uint8 as u8
from imageio.v2 import imread
from imageio.v2 import imwrite
from sys import argv
if len(argv) != 1:
    print(argv[1])
    im1 = imread(argv[1])
    h1 = len(im1)
    w1 = len(im1[0])
    im2 = imread(argv[2])
    h2 = len(im2)
    w2 = len(im2[0])
    out = argv[3]
else:
    print('no args!')
    im1 = imread('1.bmp')
    h1 = len(im1)
    w1 = len(im1[0])
    im2 = imread('2.bmp')
    h2 = len(im2)
    w2 = len(im2[0])
    out = 'res.bmp'
try:
    if h1 != h2 or w1 != w2:
        raise SystemExit
    im3 = [i for i in range(0, h1)]
    for iy in range(0, h1):
        im3[iy] = [i for i in range(0, w1)]
        for ix in range(0, w1):
            a = int(im1[iy][ix][0] + 0)/(int(im1[iy][ix][1] + 0) + 0.00001)
            b = int(im1[iy][ix][0] + 0)/(int(im1[iy][ix][2]) + 0 + 0.00001)
            v = (im2[iy][ix][0] + 0 + im2[iy][ix][1] + 0 + im2[iy][ix][2] + 0)
            im3[iy][ix] = [u8((v*a*b)//(a*b+a+b)), u8((v*b)//(a*b+a+b)), u8((v*a)//(a*b+a+b))]
    imwrite(out, im3, format='bmp')
except SystemExit:
    print("Sizes are not equal!")
