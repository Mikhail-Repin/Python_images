from scipy import ndimage
import numpy as np


def reduce(img, n):
    result = np.zeros((img.shape[0] // n, img.shape[1] // n))
    for i in range(result.shape[0]):
        for j in range(result.shape[1]):
            result[i, j] = np.mean(img[i*n:(i+1)*n, j*n:(j+1)*n])
    return result


def rotate(img, ang):
    return ndimage.rotate(img, ang, reshape=False)


def reflect(img, val):
    return img[::val, :]


def make_transform(img, direction, angle, contrast=1.0, brightness=0.0):
    return contrast*rotate(reflect(img, direction), angle) + brightness


def bright(R, D):
    A = np.concatenate((np.ones((D.size, 1)), np.reshape(D, (D.size, 1))), axis=1)
    B = np.reshape(R, (R.size,))
    x, _, _, _ = np.linalg.lstsq(A, B, rcond=None)
    return x[1], x[0]
