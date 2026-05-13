from tkinter import Image

from scipy.fft import dctn, idctn
import numpy as np
import matplotlib.pyplot as plt

import PIL.Image as Image

def calculate_dct2(F, cut_threshold, img):
    print("Calcolo DCT2...")
    print("Soglia taglio: ", cut_threshold)
    print("Immagine: ", img)
    
    numpy_image = np.array(img)    
    
    row, col = F, F
    
    row_blocks = row // F
    col_blocks = col // F
       
    c = dctn(numpy_image, type=2, norm='ortho')
        
    for k in range(row_blocks):
        for l in range(col_blocks):
            if (k + l) >= cut_threshold:
                c[k, l] = 0 # type: ignore
                
    ff = idctn(c, type=2, norm='ortho').round().astype(int) # type: ignore
    ff[ff < 0] = 0
    ff[ff > 255] = 255
    
    print("DCT2 calcolata: ", ff)
    
    image = Image.fromarray(ff.astype('uint8')) # type: ignore
    image.show()
    return image


calculate_dct2(8, 4, Image.open("./immagini/tonypitony.bmp"))