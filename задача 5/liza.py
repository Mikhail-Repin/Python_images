from PIL import Image, ImageDraw, ImageFilter
from operator import itemgetter
import numpy
import sys

def lib_edit(im):
    im2 = im.filter(ImageFilter.MedianFilter(size = 3))
    im2.save('result-lib.bmp')

def user_edit(im):
    im = im.convert("RGBA")
    data = numpy.array(im)
    #print(data)
    filter_size = 5
    temp = []
    indexer = filter_size // 2
    data_final = numpy.zeros((len(data),len(data[0]),4))
    for i in range(len(data)):

        for j in range(len(data[0])):

            for z in range(filter_size):
                if i + z - indexer < 0 or i + z - indexer > len(data) - 1:
                    for c in range(filter_size):
                        temp.append([0,0,0,0])
                else:
                    if j + z - indexer < 0 or j + indexer > len(data[0]) - 1:
                        temp.append([0,0,0,0])
                    else:
                        for k in range(filter_size):
                            temp.append(numpy.array(data[i + z - indexer][j + k - indexer]))
            tmp1 = []
            for p in range(len(temp)):
                tmp1.append((numpy.mean(temp[p]), temp[p]))
            '''for p in range(len(temp)):
                tmp1.append(numpy.mean(temp[p]))
            tmp1.sort()'''
            #print(tmp1)
            #print(tmp1[(len(temp) // 2)][0])
            data_final[i][j] = sorted(tmp1, key=itemgetter(0))[(len(temp) // 2)][1]
            #print(data_final[i][j])
            temp = []
    im2 = Image.fromarray(data_final.astype(numpy.uint8)).convert('RGB')
    im2.save('result-user.bmp')

def user_edit1(im):
    im = im.convert("L")
    data = numpy.array(im)
    filter_size = 3
    temp = []
    indexer = filter_size // 2
    data_final = []
    data_final = numpy.zeros((len(data),len(data[0])))
    for i in range(len(data)):

        for j in range(len(data[0])):

            for z in range(filter_size):
                if i + z - indexer < 0 or i + z - indexer > len(data) - 1:
                    for c in range(filter_size):
                        temp.append(0)
                else:
                    if j + z - indexer < 0 or j + indexer > len(data[0]) - 1:
                        temp.append(0)
                    else:
                        for k in range(filter_size):
                            temp.append(data[i + z - indexer][j + k - indexer])
                            #print(data[i][j])

            temp.sort()
            data_final[i][j] = temp[len(temp) // 2]
            temp = []
    im2 = Image.fromarray(data_final).convert('RGBA')
    im2.save('result-user-black-white.bmp')


def main():
    im1 = Image.open('liza.bmp')
    lib_edit(im1)

    im2 = Image.open('liza.bmp')
    user_edit(im2)

    im3 = Image.open('liza.bmp')
    user_edit1(im3)

######### main ##########
main()
