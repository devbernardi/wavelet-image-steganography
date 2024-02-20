import cv2
import numpy as np
from PIL import Image, ImageTk
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from wavelet import WaveletTransform  

#proyek untuk Uas pengolahan citra 
class AplikasiWavelet:
    def __init__(self, root):
        self.root = root
        self.root.title("Pengodek/Pemdekod Citra dengan WaveletTransform")

        self.wavelettransform = WaveletTransform()

        # Membuat Notebook (Tab)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both')

        # Menambahkan Tab Encode
        self.tab_encode = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_encode, text="Encoding")

        # Menambahkan Tab Decode
        self.tab_decode = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_decode, text="Decoding")
        #Jangan remove ini
        self.label_hak_cipta = tk.Label(self.root, text="© 2024 devbernardi github. All rights reserved.", fg="gray")
        self.label_hak_cipta.pack(side=tk.BOTTOM, pady=5)
        self.buat_widget_encode()
        self.buat_widget_decode()

    def buat_widget_encode(self):
        # Frame untuk menampilkan gambar dan melakukan encode
        self.frame_encode = tk.Frame(self.tab_encode)
        self.frame_encode.pack(pady=10)

        # Label untuk judul gambar sebelum encode
        label_sebelum_encode = tk.Label(self.frame_encode, text="Gambar Sebelum Encode")
        label_sebelum_encode.grid(row=0, column=0, padx=10)

        # Label untuk judul gambar sesudah encode
        label_sesudah_encode = tk.Label(self.frame_encode, text="Gambar Sesudah Encode")
        label_sesudah_encode.grid(row=0, column=1, padx=10)

        # Canvas untuk menampilkan gambar sebelum encode
        self.canvas_sebelum_encode = tk.Canvas(self.frame_encode, width=400, height=400)
        self.canvas_sebelum_encode.grid(row=1, column=0, padx=10)

        # Canvas untuk menampilkan gambar sesudah encode
        self.canvas_sesudah_encode = tk.Canvas(self.frame_encode, width=400, height=400)
        self.canvas_sesudah_encode.grid(row=1, column=1, padx=10)
        # Label untuk petunjuk pesan rahasia
        label_petunjuk = tk.Label(self.frame_encode, text="Masukkan text di bawah (wajib):")
        label_petunjuk.grid(row=2, column=0, columnspan=2, pady=5)

        # Entry untuk memasukkan test untuk disisipkan
        self.entry_sisipkan_pesan = tk.Entry(self.frame_encode, width=50)
        self.entry_sisipkan_pesan.grid(row=2, column=0, columnspan=2, pady=10)

        # Tombol untuk memilih gambar
        self.tombol_pilih_gambar_encode = tk.Button(self.frame_encode, text="Pilih Gambar", command=self.pilih_gambar_encode)
        self.tombol_pilih_gambar_encode.grid(row=3, column=0, columnspan=2, pady=10)

        # Tombol untuk melakukan encoding
        self.tombol_encode = tk.Button(self.frame_encode, text="Encode", command=self.encode_gambar)
        self.tombol_encode.grid(row=4, column=0, columnspan=2, pady=10)

    def buat_widget_decode(self):
        # Frame untuk menampilkan gambar yang akan di-decode
        self.frame_decode = tk.Frame(self.tab_decode)
        self.frame_decode.pack(pady=10)

        # Label untuk judul gambar yang akan di-decode
        label_gambar_decode = tk.Label(self.frame_decode, text="Gambar untuk Decode")
        label_gambar_decode.grid(row=0, column=0, padx=10)

        # Canvas untuk menampilkan gambar yang akan di-decode
        self.canvas_decode = tk.Canvas(self.frame_decode, width=400, height=400)
        self.canvas_decode.grid(row=1, column=0, padx=10)

        # Tombol untuk memilih gambar untuk decode
        self.tombol_pilih_gambar_decode = tk.Button(self.frame_decode, text="Pilih Gambar", command=self.pilih_gambar_decode)
        self.tombol_pilih_gambar_decode.grid(row=2, column=0, pady=10)

        # Label untuk judul hasil decode
        self.label_hasil_decode = tk.Label(self.frame_decode, text="Hasil Decode:")
        self.label_hasil_decode.grid(row=3, column=0, pady=10)

        # Text untuk menampilkan hasil decode
        self.text_hasil_decode = tk.Text(self.frame_decode, height=5, width=50)
        self.text_hasil_decode.grid(row=4, column=0, padx=10, pady=10)

        # Tombol untuk melakukan decoding
        self.tombol_decode = tk.Button(self.frame_decode, text="Decode", command=self.decode_gambar)
        self.tombol_decode.grid(row=5, column=0, pady=10)

    def pilih_gambar_encode(self):
        # Memilih gambar menggunakan file dialog
        path_gambar = filedialog.askopenfilename(title="Pilih Gambar untuk Encode", filetypes=[("File Gambar", "*.png;*.jpg;*.jpeg")])

        if path_gambar:
            # Menampilkan gambar pada canvas encode sebelum
            self.tampilkan_gambar(path_gambar, canvas=self.canvas_sebelum_encode)

            # Menyimpan path gambar untuk digunakan pada operasi encoding
            self.path_gambar_encode = path_gambar

    def pilih_gambar_decode(self):
        # Memilih gambar menggunakan file dialog
        path_gambar = filedialog.askopenfilename(title="Pilih Gambar untuk Decode", filetypes=[("File Gambar", "*.png;*.jpg;*.jpeg")])

        if path_gambar:
            # Menampilkan gambar yang akan di-decode pada canvas decode
            self.tampilkan_gambar(path_gambar, canvas=self.canvas_decode)

            # Menyimpan path gambar untuk digunakan pada operasi decoding
            self.path_gambar_decode = path_gambar

    def encode_gambar(self):
        if hasattr(self, 'path_gambar_encode'):
            # Memastikan ada path gambar yang telah dipilih
            sisipkan_pesan = self.entry_sisipkan_pesan.get()

            if sisipkan_pesan:
                # encoding sisipkan_pesan ke dalam gambar
                gambar = cv2.imread(self.path_gambar_encode)
                gambar_encoded = self.wavelettransform.encoding_gambar(gambar, sisipkan_pesan)

                # Meminta lokasi penyimpanan dari pengguna
                path_simpan = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("File PNG", "*.png"), ("File JPEG", "*.jpg"), ("Semua file", "*.*")])

                if path_simpan:
                    # Menyimpan gambar yang telah diencode dan menampilkannya pada canvas encode sesudah
                    cv2.imwrite(path_simpan, gambar_encoded)
                    self.tampilkan_gambar(path_simpan, canvas=self.canvas_sesudah_encode)
                    messagebox.showinfo("Info", "Gambar yang diencode berhasil disimpan.")
                else:
                    messagebox.showwarning("Peringatan", "Penyimpanan dibatalkan.")
            else:
                messagebox.showwarning("Peringatan", "Masukkan text sebelum melakukan encoding.")
        else:
            messagebox.showwarning("Peringatan", "Pilih gambar terlebih dahulu.")
            #https://github.com/devbernardi/wavelet-image-steganography

    def decode_gambar(self):
        if hasattr(self, 'path_gambar_decode'):
            # Memastikan ada path gambar yang telah dipilih
            gambar = cv2.imread(self.path_gambar_decode)
            pesan_didecode = self.wavelettransform.decoding_gambar(gambar)

            # Menampilkan pesan yang telah didecode
            self.text_hasil_decode.delete(1.0, tk.END)
            self.text_hasil_decode.insert(tk.END, pesan_didecode)
        else:
            messagebox.showwarning("Peringatan", "Pilih gambar terlebih dahulu.")

    def tampilkan_gambar(self, path_gambar, canvas=None):
        # Membaca gambar menggunakan OpenCV dan mengonversinya ke format Tkinter PhotoImage
        img = cv2.imread(path_gambar)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = img.resize((400, 400), Image.ANTIALIAS if hasattr(Image, 'ANTIALIAS') else Image.BICUBIC)
        tk_img = ImageTk.PhotoImage(img)

        # Menampilkan gambar pada canvas yang diberikan atau canvas utama jika tidak disediakan
        if canvas:
            canvas.config(width=tk_img.width(), height=tk_img.height())
            canvas.create_image(0, 0, anchor=tk.NW, image=tk_img)
            canvas.image = tk_img

            # Menambahkan label informasi di bawah canvas dengan latar belakang hitam
            label_info = tk.Label(canvas, text=f"Dimensi: {img.width} x {img.height}\nUkuran File: {self.get_file_size(path_gambar)} KB", fg="white", bg="black", font=("Arial", 10))
            canvas.create_window(10, tk_img.height()-10 , anchor=tk.W, window=label_info)

        else:
            self.canvas_decode.config(width=tk_img.width(), height=tk_img.height())
            self.canvas_decode.create_image(0, 0, anchor=tk.NW, image=tk_img)
            self.canvas_decode.image = tk_img

            # Menambahkan label informasi di bawah canvas dengan latar belakang hitam
            label_info = tk.Label(self.canvas_decode, text=f"Dimensi: {img.width} x {img.height}\nUkuran File: {self.get_file_size(path_gambar)} KB", fg="white", bg="black", font=("Arial", 10))
            self.canvas_decode.create_window(10, tk_img.height()-10, anchor=tk.W, window=label_info)

    def get_file_size(self, file_path):
        # Fungsi untuk mendapatkan ukuran file dalam KB
        return round(os.path.getsize(file_path) / 1024, 2)
if __name__ == "__main__":
    root = tk.Tk()
    app = AplikasiWavelet(root)
    root.mainloop()
