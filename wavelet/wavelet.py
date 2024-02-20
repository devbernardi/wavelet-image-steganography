import cv2
import numpy as np

class WaveletTransform:
    def encoding_gambar(self, gambar, sisipkan_teks):
        # Mendapatkan ukuran baris dan kolom dari gambar
        baris, kolom = gambar.shape[:2]
        
        # Menghitung panjang yang diperlukan untuk pesan
        panjang_diperlukan = len(sisipkan_teks) + 4  # 4 byte untuk panjang pesan

        # Periksa apakah perlu meresize gambar
        if baris % 8 != 0 or kolom % 8 != 0 or baris * kolom < panjang_diperlukan:
            kolom_baru = max(kolom, panjang_diperlukan // baris + 1)
            gambar = cv2.resize(gambar, (kolom_baru + (8 - kolom_baru % 8), baris + (8 - baris % 8)))
        
        # Memisahkan saluran warna gambar menjadi saluran biru, hijau, dan merah
        bImg, gImg, rImg = cv2.split(gambar)
        
        # Melakukan Inverse Wavelet Transform (IWT) pada saluran warna biru
        bImg = self.iwt2(bImg)
    
        # Dapatkan ukuran gambar yang telah dipadding dalam piksel
        tinggi, lebar = bImg.shape[:2]
    
        # Atur pixel pertama sebagai panjang sisipkan_teks
        panjang_bytes = len(sisipkan_teks).to_bytes(4, byteorder='big')
        for i in range(4):
            gambar[0, i, 0] = panjang_bytes[i]
    
        # Enkode pesan
        indeks = 4  # Mulai dari pixel keempat
        for baris in range(1, tinggi):
            for kolom in range(lebar):
                r, g, b = gambar[baris, kolom]
                
                if indeks < len(sisipkan_teks) + 4:
                    karakter = sisipkan_teks[indeks - 4]
                    asc = ord(karakter)
                else:
                    asc = r
    
                gambar[baris, kolom, 0] = asc  # Modifikasi nilai saluran biru
                indeks += 1
    
        return gambar

    def decoding_gambar(self, gambar):
        # Mengambil panjang pesan dari empat pixel pertama
        panjang_bytes = [gambar[0, i, 0] for i in range(4)]
        panjang_pesan = int.from_bytes(panjang_bytes, byteorder='big')
        pesan = ""
        baris, kolom = gambar.shape[:2]
    
        indeks = 4  # Mulai dari pixel keempat
        for r in range(1, baris):
            for c in range(kolom):
                if indeks < panjang_pesan + 4:
                    pesan += chr(gambar[r, c, 0])
                indeks += 1
    
                if indeks > panjang_pesan + 4:
                    break
    
            if indeks > panjang_pesan + 4:
                break
    
        return pesan

    def iwt2(self, array):
        # Transformasi gelombang diskrit 2 dimensi
        return self._iwt(self._iwt(array.astype(int)).T).T

    def iiwt2(self, array):
        # Inverse 
        return self._iiwt(self._iiwt(array.astype(int).T).T)

    def _iwt(self, array):
        # Transformasi gelombang diskrit 1 dimensi ke arah vertikal
        output = np.zeros_like(array)
        nx, ny = array.shape
        x = nx // 2
        for j in range(ny):
            output[0:x, j] = (array[0::2, j] + array[1::2, j]) // 2
            output[x:nx, j] = array[0::2, j] - array[1::2, j]
        return output

    def _iiwt(self, array):
        # Inverse ke arah vertikal
        output = np.zeros_like(array)
        nx, ny = array.shape
        x = nx // 2
        for j in range(ny):
            output[0::2, j] = array[0:x, j] + (array[x:nx, j] + 1) // 2
            output[1::2, j] = output[0::2, j] - array[x:nx, j]
        return output