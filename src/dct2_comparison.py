import numpy as np
import time
import matplotlib.pyplot as plt
from scipy.fft import dctn

from dct2_implementation import dct_2D

def run_benchmark():
    # Dimensioni N degli array quadrati (N x N)
    N_sizes = list(range(1000, 35000, 5000))  # Da 1000 a 35000 con passo di 5000
    
    times_manual = []
    times_fast = []

    print(f"{'N':<10} | {'Manuale (s)':<15} | {'Fast (s)':<15}")
    print("-" * 45)

    for N in N_sizes:
        # Creiamo un array quadrato casuale
        f_mat = np.random.rand(N, N)

        # Misura tempo: dct_2D implementazione manuale
        start = time.time()
        dct_2D(f_mat)
        t_m = time.time() - start
        times_manual.append(t_m)

        # Misura tempo: VERSIONE FAST (Scipy)
        start = time.time()
        # norm='ortho' per coerenza con compute_D
        dctn(f_mat, type=2, norm='ortho')
        t_f = time.time() - start
        times_fast.append(t_f)

        print(f"{N:<5} | {t_m:<10.5f} | {t_f:<10.5f}")


    # --- GENERAZIONE GRAFICO ---
    
    plt.figure(figsize=(10, 6))
    
   
     # Scala semilogaritmica
    plt.plot(N_sizes, times_manual, 'o-', label='DCT2 Fatta in casa ($O(N^3)$)', linewidth=2)
    plt.plot(N_sizes, times_fast, 's-', label='DCT2 Scipy Fast ($O(N^2 \log N)$)', linewidth=2)
    plt.yscale('log')
    plt.title('Confronto Tempi di Esecuzione DCT2')
    plt.xlabel('Dimensione del lato della matrice (N)')
    plt.ylabel('Tempo (secondi) - Scala Log')
    plt.grid()
    plt.legend()
    
    plt.savefig("benchmark_dct2.png", dpi=300, bbox_inches='tight')


    plt.show()

if __name__ == "__main__":
    run_benchmark()