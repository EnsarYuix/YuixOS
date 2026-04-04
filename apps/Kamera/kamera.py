import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
import os
import time
from datetime import datetime

class YuixKameraFinal:
    def __init__(self, root):
        self.root = root
        self.root.title("YuixOS Pro Camera")
        self.root.geometry("450x850")
        self.root.configure(bg="#0f0f0f")

        self.save_path = "../../galeri"
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)

        # Kamera Ayarları
        self.kamera_id = 0  # Varsayılan kamera
        self.cap = cv2.VideoCapture(self.kamera_id)
        self.kayit_yapiliyor = False
        self.video_yazici = None
        self.baslangic_zamani = 0
        
        # Kamera Ekranı
        self.video_label = tk.Label(self.root, bg="black", bd=0)
        self.video_label.pack(fill="both", expand=True, pady=(0, 10))

        # Kayıt Süresi Etiketi
        self.bilgi_label = tk.Label(self.root, text="", fg="red", bg="black", font=("Consolas", 14, "bold"))
        self.bilgi_label.place(x=20, y=20)

        # Alt Kontrol Barı
        self.alt_bar = tk.Frame(self.root, bg="#1a1a1a", height=180)
        self.alt_bar.pack(fill="x", side="bottom")

        # --- BUTONLAR ---
        # Fotoğraf Butonu
        self.foto_btn = tk.Button(self.alt_bar, text="📸", font=("Arial", 28), fg="white", bg="#333", 
                                 activebackground="#555", bd=0, width=3, command=self.foto_cek)
        self.foto_btn.place(relx=0.5, rely=0.4, anchor="center")

        # Video Butonu
        self.video_btn = tk.Button(self.alt_bar, text="🎥", font=("Arial", 22), fg="white", bg="#c0392b", 
                                  activebackground="#e74c3c", bd=0, width=3, command=self.video_kontrol)
        self.video_btn.place(relx=0.2, rely=0.4, anchor="center")

        # KAMERA DEĞİŞTİRME BUTONU (YENİ!)
        self.cevir_btn = tk.Button(self.alt_bar, text="🔄", font=("Arial", 22), fg="white", bg="#2980b9", 
                                   activebackground="#3498db", bd=0, width=3, command=self.kamera_degistir)
        self.cevir_btn.place(relx=0.8, rely=0.4, anchor="center")

        self.akisi_guncelle()

    def akisi_guncelle(self):
        ret, frame = self.cap.read()
        if ret:
            # Ön kamera hissi için görüntüyü çevir
            frame = cv2.flip(frame, 1)
            
            if self.kayit_yapiliyor and self.video_yazici:
                self.video_yazici.write(frame)
                gecen_sure = int(time.time() - self.baslangic_zamani)
                self.bilgi_label.config(text=f"● KAYIT {gecen_sure//60:02d}:{gecen_sure%60:02d}")

            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            img = img.resize((450, 600), Image.Resampling.LANCZOS)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)
        
        self.root.after(10, self.akisi_guncelle)

    def kamera_degistir(self):
        # Mevcut kamerayı kapat
        self.cap.release()
        
        # Diğer kameraya geç (0'dan 1'e veya 1'den 0'a)
        self.kamera_id = 1 if self.kamera_id == 0 else 0
        self.cap = cv2.VideoCapture(self.kamera_id)
        
        # Kamera desteklenmiyorsa geri dön
        if not self.cap.isOpened():
            self.kamera_id = 0
            self.cap = cv2.VideoCapture(self.kamera_id)
            messagebox.showwarning("YuixOS", "Başka kamera bulunamadı veya desteklenmiyor!")

    def foto_cek(self):
        self.video_label.config(bg="white")
        self.root.after(100, lambda: self.video_label.config(bg="black"))
        ret, frame = self.cap.read()
        if ret:
            dosya = f"FOTO_{datetime.now().strftime('%H%M%S')}.jpg"
            cv2.imwrite(os.path.join(self.save_path, dosya), frame)

    def video_kontrol(self):
        if not self.kayit_yapiliyor:
            dosya = f"VIDEO_{datetime.now().strftime('%H%M%S')}.mp4"
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            self.video_yazici = cv2.VideoWriter(os.path.join(self.save_path, dosya), fourcc, 20.0, (640, 480))
            self.baslangic_zamani = time.time()
            self.kayit_yapiliyor = True
            self.video_btn.config(text="⏹️", bg="#f39c12")
        else:
            self.kayit_yapiliyor = False
            if self.video_yazici:
                self.video_yazici.release()
            self.video_btn.config(text="🎥", bg="#c0392b")
            self.bilgi_label.config(text="")
            messagebox.showinfo("YuixOS", "Video Galeriye Eklendi!")

if __name__ == "__main__":
    root = tk.Tk()
    app = YuixKameraFinal(root)
    root.mainloop()