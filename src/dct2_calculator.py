import io
import numpy as np
from scipy.fft import dctn, idctn
import PIL.Image as Image


def calculate_dct2(F: int, cut_threshold: int, img: Image.Image) -> bytes:

    img_gray = img.convert('L')
    numpy_image = np.array(img_gray, dtype=float)

    H, W = numpy_image.shape

    # Suddivide l'immagine in blocchi e scarta gli avanzi
    n_row_blocks = H // F
    n_col_blocks = W // F

    H_crop = n_row_blocks * F
    W_crop = n_col_blocks * F
    cropped = numpy_image[:H_crop, :W_crop] # Immagine senza gli avanzi

    print("\n")
    print(f"Numero di blocchi: {n_row_blocks}x{n_col_blocks} = {n_row_blocks * n_col_blocks}")
    print(f"Immagine ritagliata: {W_crop}x{H_crop} pixel (avanzi scartati: {H - H_crop} righe, {W - W_crop} colonne)")
    print("\n")

    result = np.empty_like(cropped) # Array vuoto per i risultati

    for i in range(n_row_blocks):
        for j in range(n_col_blocks):

            # Estrae il blocco F x F (i*F = inizio, (i+1)*F = fine)
            block = cropped[i*F:(i+1)*F, j*F:(j+1)*F]

            c = dctn(block, type=2, norm='ortho')

            for k in range(F):
                for l in range(F):
                    if k + l >= cut_threshold:
                        c[k, l] = 0 # type: ignore

            # DCT2 inversa
            ff = idctn(c, type=2, norm='ortho')

            ff = np.clip(np.round(ff), 0, 255) # type: ignore

            result[i*F:(i+1)*F, j*F:(j+1)*F] = ff

    result_image = Image.fromarray(result.astype('uint8'), mode='L')
    buffer = io.BytesIO()
    result_image.save(buffer, format='png')

    print(f"Peso finale con soglia d={cut_threshold}: {len(buffer.getvalue()) / 1024:.2f} KB")

    return buffer.getvalue()
