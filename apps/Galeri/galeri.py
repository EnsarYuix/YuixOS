import tkinter as tk
from tkinter import messagebox
import os
from PIL import Image, ImageTk

class YuixGaleriPro:
    def __init__(self, root):
        self.root = root
        self.root.title("YuixOS Galeri Pro")
        self.root.geometry("450x850")
        self.root.configure(bg="#0f0f0f")

        self.galeri_yolu = "../../galeri"
        if not os.path.exists(self.galeri_yolu):
            os.makedirs(self.galeri_yolu)

        # Üst Bar
        self.ust_bar = tk.Frame(self.root, bg="#1a1a1a", height=70)
        self.ust_bar.pack(fill="x")
        self.ust_bar.pack_propagate(False)

        tk.Label(self.ust_bar, text="GALERİ", fg="white", bg="#1a1a1a", font=("Arial", 14, "bold")).pack(side="left", padx=20)

        self.ana_frame = tk.Frame(self.root, bg="#0f0f0f")
        self.ana_frame.pack(fill="both", expand=True)

        self.galeriyi_tazele()

    def galeriyi_tazele(self):
        for widget in self.ana_frame.winfo_children():
            widget.destroy()
        
        dosyalar = [f for f in os.listdir(self.galeri_yolu) if f.lower().endswith((".png", ".jpg", ".jpeg"))]

        if not dosyalar:
            tk.Label(self.ana_frame, text="Hadi, Fotoğraf çekilerek\nanılarını sakla!", 
                     fg="#555", bg="#0f0f0f", font=("Arial", 14, "italic")).place(relx=0.5, rely=0.5, anchor="center")
        else:
            canvas = tk.Canvas(self.ana_frame, bg="#0f0f0f", highlightthickness=0)
            scrollbar = tk.Scrollbar(self.ana_frame, orient="vertical", command=canvas.yview)
            scroll_frame = tk.Frame(canvas, bg="#0f0f0f")

            scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
            canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            r, s = 0, 0
            for dosya in dosyalar:
                try:
                    yol = os.path.join(self.galeri_yolu, dosya)
                    img = Image.open(yol)
                    img.thumbnail((130, 130))
                    ph = ImageTk.PhotoImage(img)

                    lbl = tk.Label(scroll_frame, image=ph, bg="#0f0f0f", bd=2, cursor="hand2")
                    lbl.image = ph
                    lbl.grid(row=r, column=s, padx=7, pady=7)
                    
                    # Tıklayınca tam ekran aç
                    lbl.bind("<Button-1>", lambda e, p=yol: self.tam_ekran_ac(p))
                    
                    s += 1
                    if s > 2: s = 0; r += 1
                except: continue

    def tam_ekran_ac(self, foto_yolu):
        top = tk.Toplevel(self.root)
        top.title("Fotoğraf Önizleme")
        top.geometry("450x850")
        top.configure(bg="black")

        # Fotoğrafı pencereye sığdır
        img = Image.open(foto_yolu)
        img.thumbnail((450, 700))
        ph = ImageTk.PhotoImage(img)

        img_label = tk.Label(top, image=ph, bg="black")
        img_label.image = ph
        img_label.pack(expand=True)

        # Alt kısma silme butonu
        btn_frame = tk.Frame(top, bg="#1a1a1a", height=80)
        btn_frame.pack(fill="x", side="bottom")

        def foto_sil_ve_kapat():
            if messagebox.askyesno("YuixOS", "Bu fotoğraf silinsin mi?"):
                os.remove(foto_yolu)
                top.destroy()
                self.galeriyi_tazele()

        tk.Button(btn_frame, text="🗑️ BU FOTOĞRAFI SİL", fg="white", bg="#e74c3c", 
                  font=("Arial", 12, "bold"), bd=0, command=foto_sil_ve_kapat).pack(expand=True, fill="both")

if __name__ == "__main__":
    root = tk.Tk()
    app = YuixGaleriPro(root)
    root.mainloop()