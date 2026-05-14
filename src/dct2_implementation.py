import numpy as np

# Input: N grandezza del vettore da trasformare
# Output: D matrice di trasformazione
def compute_D(N):
    # Pre allocazione di D
    D = np.zeros((N, N))
    alpha_vect = np.ones(N) * np.sqrt(2/N)
    alpha_vect[0] = np.sqrt(1/N)
    
    for k in range(N):
        for i in range(N):
            D[k, i] = alpha_vect[k] * np.cos((k * np.pi * (2*i + 1)) / (2*N))
    return D
# Questa non serve ma l'ho messa per ora per chiarezza, poi la eliminerò
def dct_1D(f_vect):
    N = len(f_vect)
    D = compute_D(N)
    return D @ f_vect  # '@' esegue il prodotto matrice-vettore in numpy

def dct_2D(f_mat):
    N = f_mat.shape[0]
    D = compute_D(N)
    
    # 1. DCT1 sulle colonne: D * f_mat
    # D @ f_mat applica D a ogni colonna di f_mat
    c_mat = D @ f_mat
    
    # 2. DCT1 sulle righe: c_mat * D.T
    # Moltiplicare a destra per la trasposta equivale ad applicare D alle righe
    c_mat = c_mat @ D.T
    
    return c_mat