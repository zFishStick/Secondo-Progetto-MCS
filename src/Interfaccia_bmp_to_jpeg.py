import io
import tkinter as tk
from tkinter import filedialog, messagebox

from PIL import Image, ImageTk

from dct2_calculator import calculate_dct2


class ZoomPanCanvas(tk.Canvas):

    def __init__(self, parent):
        super().__init__(parent, bg="white")
        self.zoom = 1.0
        self.original_image = None
        self.tk_image = None
        self.image_id = None
        self.last_x = 0
        self.last_y = 0

        self.bind("<ButtonPress-1>", self.start_move)
        self.bind("<B1-Motion>",     self.do_move)
        self.bind("<MouseWheel>",    self.do_zoom)
        self.bind("<Button-4>",      self.do_zoom)
        self.bind("<Button-5>",      self.do_zoom)

    def start_move(self, event):
        self.last_x, self.last_y = event.x, event.y

    def do_move(self, event):
        dx, dy = event.x - self.last_x, event.y - self.last_y
        self.move(self.image_id, dx, dy)
        self.last_x, self.last_y = event.x, event.y

    def do_zoom(self, event):
        if event.delta > 0 or event.num == 4:
            self.zoom *= 1.1
        else:
            self.zoom /= 1.1
        self._render()

    def load_image(self, image_path: str):
        with open(image_path, "rb") as f:
            self.load_image_from_bytes(f.read())

    def load_image_from_bytes(self, image_bytes: bytes):
        self.original_image = Image.open(io.BytesIO(image_bytes))
        self.zoom = 1.0
        self._render()

    def _render(self):
        if self.original_image is None:
            return
        new_size = (
            max(1, int(self.original_image.width  * self.zoom)),
            max(1, int(self.original_image.height * self.zoom)),
        )
        resized = self.original_image.resize(new_size, Image.LANCZOS) # type: ignore
        self.tk_image = ImageTk.PhotoImage(resized)
        if self.image_id is None:
            self.image_id = self.create_image(0, 0, image=self.tk_image, anchor="nw")
        else:
            self.itemconfig(self.image_id, image=self.tk_image)


def select_file(canvas: ZoomPanCanvas):
    filepath = filedialog.askopenfilename(
        title="Seleziona un file .bmp",
        filetypes=[("File BMP", "*.bmp"), ("Tutti i file", "*.*")],
    )
    if filepath:
        canvas.load_image(filepath)
        print(f"Immagine caricata: {filepath}")
        print(f"Dimensione immagine: {canvas.original_image.width}x{canvas.original_image.height} pixel") # type: ignore
        print(f"Dimensione immagine (Mb): {canvas.original_image.width * canvas.original_image.height * len(canvas.original_image.getbands()) / (1024 * 1024):.2f} MB") # type: ignore


def execute_conversion(block_size_entry, cut_threshold_entry,
                       canvas_bmp: ZoomPanCanvas, canvas_jpeg: ZoomPanCanvas):
    try:
        F = int(block_size_entry.get())
        if F <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Errore", "Dimensione blocco non valida. Inserisci un intero positivo.")
        return

    limit = 2 * F - 2
    try:
        d = int(cut_threshold_entry.get())
        if d < 0 or d > limit:
            raise ValueError
    except ValueError:
        messagebox.showerror("Errore", f"Soglia taglio non valida. Inserisci un intero tra 0 e {limit}.")
        return

    if canvas_bmp.original_image is None:
        messagebox.showerror("Errore", "Nessuna immagine caricata.")
        return

    result_bytes = calculate_dct2(F, d, canvas_bmp.original_image)
    canvas_jpeg.load_image_from_bytes(result_bytes)
    print("Conversione eseguita con successo.")
    print(f"Dimensione immagine originale: {canvas_bmp.original_image.width}x{canvas_bmp.original_image.height} pixel") # type: ignore
    print(f"Dimensione immagine compressa: {len(result_bytes) / (1024 * 1024):.2f} MB")
    

def save_compressed_image(canva):
    if canva.original_image is None:
        messagebox.showerror("Errore", "Nessuna immagine da salvare.")
        return
    
    save_path = filedialog.asksaveasfilename(
        title="Salva immagine compressa",
        defaultextension=".png",
        filetypes=[("File PNG", "*.png")]
    )

    if save_path:
        canva.original_image.save(save_path, format="PNG")
        print(f"Immagine compressa salvata come: {save_path}")

        
def main():
    root = tk.Tk()
    root.title("Compressione DCT2 – Progetto MCS")
    root.geometry("1200x800")

    root.grid_rowconfigure(0, weight=0)
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    canvas_bmp  = ZoomPanCanvas(root)
    canvas_jpeg = ZoomPanCanvas(root)
    canvas_bmp .grid(row=1, column=0, sticky="nsew")
    canvas_jpeg.grid(row=1, column=1, sticky="nsew")

    toolbar = tk.Frame(root, bd=1, relief=tk.RAISED)
    toolbar.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

    tk.Button(
        toolbar, text="Carica immagine BMP",
        command=lambda: select_file(canvas_bmp)
    ).pack(side=tk.LEFT, padx=5, pady=5)

    tk.Label(toolbar, text="Dimensione blocco F:").pack(side=tk.LEFT, padx=(10, 2), pady=5)
    block_size_var = tk.IntVar(value=8)
    block_size_entry = tk.Entry(toolbar, width=5, textvariable=block_size_var)
    block_size_entry.pack(side=tk.LEFT, pady=5)

    tk.Label(toolbar, text="Soglia taglio d:").pack(side=tk.LEFT, padx=(10, 2), pady=5)
    cut_threshold_var = tk.IntVar(value=4)
    cut_threshold_entry = tk.Entry(toolbar, width=5, textvariable=cut_threshold_var)
    cut_threshold_entry.pack(side=tk.LEFT, pady=5)

    tk.Button(
        toolbar, text="Esegui compressione",
        command=lambda: execute_conversion(
            block_size_entry, cut_threshold_entry, canvas_bmp, canvas_jpeg
        )
    ).pack(side=tk.LEFT, padx=10, pady=5)

    tk.Button(
        toolbar, text="Salva immagine compressa",
        command=lambda: save_compressed_image(canvas_jpeg)
    ).pack(side=tk.LEFT, padx=10, pady=5)

    root.mainloop()


if __name__ == "__main__":
    main()