from matplotlib import colormaps, image
from matplotlib.colors import Normalize, to_hex
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog
from tkinter import messagebox 
from sympy import root

import io

from dct2_calculator import calculate_dct2

class ZoomPanCanvas(tk.Canvas):

    def __init__(self, parent, image_path):
        super().__init__(parent, bg="white")
        self.image_path = image_path
        self.grid(row=0, column=2, sticky="nsew")
        self.zoom = 1.0

        self.original_image = None
        self.tk_image = None
        self.image_id = None

        if image_path:
            self.load_image(image_path)

        self.bind("<ButtonPress-1>", self.start_move)
        self.bind("<B1-Motion>", self.do_move)
        self.bind("<MouseWheel>", self.do_zoom)
        self.bind("<Button-4>", self.do_zoom)
        self.bind("<Button-5>", self.do_zoom) 

        self.last_x = 0
        self.last_y = 0

    def start_move(self, event):
        self.last_x = event.x
        self.last_y = event.y

    def do_move(self, event):
        dx = event.x - self.last_x
        dy = event.y - self.last_y
        self.move(self.image_id, dx, dy)
        self.last_x = event.x
        self.last_y = event.y

    def do_zoom(self, event):
        if event.delta > 0 or event.num == 4:
            self.zoom *= 1.1
        elif event.delta < 0 or event.num == 5:
            self.zoom /= 1.1
        
        new_size = (
            int(self.original_image.width * self.zoom), # type: ignore
            int(self.original_image.height * self.zoom) # type: ignore
        )
        resized_image = self.original_image.resize(new_size, Image.LANCZOS) # type: ignore
        self.tk_image = ImageTk.PhotoImage(resized_image)
        self.itemconfig(self.image_id, image=self.tk_image)  # type: ignore

    def load_image_from_bytes(self, image_bytes):
        self.original_image = Image.open(io.BytesIO(image_bytes))
        resized_image = self.original_image.resize(
            (int(self.original_image.width * self.zoom),
             int(self.original_image.height * self.zoom)),
            Image.LANCZOS) # type: ignore
        self.tk_image = ImageTk.PhotoImage(resized_image)
        if self.image_id is None:
            self.image_id = self.create_image(0, 0, image=self.tk_image, anchor="nw")
        else:
            self.itemconfig(self.image_id, image=self.tk_image)

    def reload_image(self):
        if self.original_image:
            self.load_image_from_bytes(self.original_image.tobytes())

    def load_image(self, image_path):
        with open(image_path, "rb") as f:
            self.load_image_from_bytes(f.read())

def select_file(canvas):
    filepath = filedialog.askopenfilename(
        title="Seleziona un file .bmp",
        filetypes=[("File bmp", "*.bmp"), ("Tutti i file", "*.*")]
    )
    if filepath:
        canvas.load_image(filepath)
        
def set_block_size(entry):
    try:
        block_size = int(entry.get())
        if block_size <= 0:
            messagebox.showerror("Errore", "Dimensione blocco non valida. Inserisci un numero intero positivo.")
            return None
        return block_size
    except ValueError:
        messagebox.showerror("Errore", "Dimensione blocco non valida. Inserisci un numero intero.")
        return None
    
def set_cut_threshold(entry, block_size):
    limit = (2 * block_size) - 2
    try:
        cut_threshold = int(entry.get())
        if cut_threshold < 0 or cut_threshold > limit:
            messagebox.showerror("Errore", f"Soglia taglio non valida. Inserisci un numero intero tra 0 e {limit}.")
            return None
        return cut_threshold
    except ValueError:
        messagebox.showerror("Errore", "Soglia taglio non valida. Inserisci un numero intero.")
        return None
    
def execute_conversion(block_size_entry, cut_threshold_entry, canvas_bmp, canvas_jpeg):
    try:
        block_size = set_block_size(block_size_entry)
        if block_size is None:
            return    
        
        cut_threshold = set_cut_threshold(cut_threshold_entry, block_size)
        
        if cut_threshold is None:
            return
        
        if canvas_bmp.original_image is None:
            messagebox.showerror("Errore", "Nessuna immagine caricata. Carica un'immagine bmp prima di eseguire la conversione.")
            return  
        
        result = calculate_dct2(block_size, cut_threshold, canvas_bmp.original_image)
        canvas_jpeg.load_image_from_bytes(result)
        print("Conversione eseguita con successo.")

    except ValueError:
        messagebox.showerror("Errore", "Inserisci tutti i parametri per eseguire la conversione.")
        return
        
def main():
    
    root = tk.Tk()
    root.geometry("1200x800")
    root.grid_rowconfigure(0, weight=0)
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    
    block_size = tk.IntVar(value=8)
    cut_threshold = tk.IntVar(value=4)
    image = None

    canvas_bmp = ZoomPanCanvas(root, None)
    canvas_bmp.grid(row=1, column=0, sticky="nsew")

    canvas_jpeg = ZoomPanCanvas(root, None)
    canvas_jpeg.grid(row=1, column=1, sticky="nsew")

    toolbar = tk.Frame(root, bd=1, relief=tk.RAISED)
    toolbar.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

    btn_select = tk.Button(toolbar, text="Carica immagine bmp", command=lambda: select_file(canvas_bmp))
    btn_select.pack(side=tk.LEFT, padx=5, pady=5)
    
    block_size_label = tk.Label(toolbar, text="Dimensione blocco:")
    block_size_entry = tk.Entry(toolbar, width=5, textvariable=block_size)
    
    cut_treshold_label = tk.Label(toolbar, text="Soglia taglio:")
    cut_treshold_entry = tk.Entry(toolbar, width=5, textvariable=cut_threshold)
    
    block_size_label.pack(side=tk.LEFT, padx=5, pady=5)
    block_size_entry.pack(side=tk.LEFT, padx=5, pady=5)
    
    cut_treshold_label.pack(side=tk.LEFT, padx=5, pady=5)
    cut_treshold_entry.pack(side=tk.LEFT, padx=5, pady=5)
    
    execute_button = tk.Button(toolbar, text="Esegui conversione", command=lambda: execute_conversion(block_size_entry, cut_treshold_entry, canvas_bmp, canvas_jpeg))
    execute_button.pack(side=tk.LEFT, padx=5, pady=5)

    root.mainloop()
    return

if __name__ == "__main__":
    main()
