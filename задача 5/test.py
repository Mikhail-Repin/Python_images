import numpy as np
def r2(y_true, y_pred):
    N = y_true.shape[0]
    a = y_pred - y_true
    b = y_true - np.mean(y_true)*np.ones((1,N))
    De = 1/N * np.dot(a, a.T)
    Dz = 1/N * np.dot(b, b.T)
    return float(1 - De/Dz)
y = np.array([0,1, 3])
x = y + 1
print(r2(x, y))
