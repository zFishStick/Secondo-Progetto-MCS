import numpy as np
from scipy.fft import dctn
def test_dct_2D():
    f_mat = np.array([[231, 32, 233, 161, 24, 71, 140, 245],
                      [247, 40, 248, 245, 124, 204, 36, 107],
                      [234, 202, 245, 167, 9, 217, 239, 173],
                      [193, 190, 100, 167, 43, 180, 8, 70],
                      [11, 24, 210, 177, 81, 243, 8, 112],
                      [97, 195, 203, 47, 125, 114, 165, 181],
                      [193, 70, 174, 167, 41, 30, 127, 245],
                      [87, 149, 57, 192, 65, 129, 178, 228]])
    c_2d = dctn(f_mat, type=2, norm='ortho')
    print("Matrice dei coefficienti DCT2:")
    print(np.round(c_2d, 2))

def test_dct_1D():
    f_vect = np.array([231, 32, 233, 161, 24, 71, 140, 245])
    c_1d = dctn(f_vect, type=2, norm='ortho')
    print("Vettore dei coefficienti DCT1:")
    print(np.round(c_1d, 2))

if __name__ == "__main__":
    test_dct_2D()
    test_dct_1D()