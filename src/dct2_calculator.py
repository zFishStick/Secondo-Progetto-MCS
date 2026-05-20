import io
from tkinter import Image

from scipy.fft import dctn, idctn
import numpy as np
import matplotlib.pyplot as plt

import PIL.Image as Image

def calculate_dct2(F, cut_threshold, img):
    print("Calcolo DCT2...")
    print("Soglia taglio: ", cut_threshold)
    print("Immagine: ", img)

    img = img.convert('L')  # Converti l'immagine in scala di grigi
    numpy_image = np.array(img)    
    row, col = numpy_image.shape
    
    row_blocks = row // F #divisione per ottenere il numero dei blocchi
    col_blocks = col // F #divisione per ottenere il numero dei blocchi

    output_image = np.zeros((row_blocks * F, col_blocks * F), dtype=np.uint8) #preallocazione dell'immagine di output
   
    for row_block in range(row_blocks):
        for col_block in range(col_blocks):
            #calcolo dell dct2 blocco per blocco
            block = numpy_image[row_block*F:(row_block+1)*F, col_block*F:(col_block+1)*F]
            c = dctn(block, type=2, norm='ortho')
        
            #applico la soglia di taglio
            for k in range(F):
                for l in range(F):
                    if (k + l) >= cut_threshold:
                        c[k, l] = 0
                
            #ricostruisco il blocco con l'idct2    
            ff = idctn(c, type=2, norm='ortho').round().astype(int)
            #clipping dei valori per evitare di uscire dall'intervallo [0, 255]
            ff[ff < 0] = 0
            ff[ff > 255] = 255
            #inserisco il blocco ricostruito nell'immagine di output
            output_image[row_block*F:(row_block+1)*F, col_block*F:(col_block+1)*F] = ff
    
    print("DCT2 calcolata: ", output_image)
    
    image = Image.fromarray(output_image.astype('uint8'))
    #image.show()
    buffer = io.BytesIO()
    image.save(buffer, format="BMP")
    image_bytes = buffer.getvalue()
    buffer.close()
    return image_bytes


#calculate_dct2(8, 4, Image.open("./immagini/tonypitony.bmp"))