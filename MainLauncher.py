import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess
import os
import time

# --- 1. BOOT EKRANI (SENİN TASARIMIN) ---
class YuixOS_Boot:
    def __init__(self, root, on_complete):
        self.root = root
        self.on_complete = on_complete
        self.root.overrideredirect(True)
        self.root.geometry("450x850")
        self.root.configure(bg="black")
        
        # Ekranı ortala
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f"450x850+{(sw//2)-225}+{(sh//2)-425}")

        self.base = r"C:\Users\LBH-MUSTAFA\Desktop\YuixOS"
        # boot_logo.png senin image_bad572.png tasarımın olmalı
        self.boot_img_path = os.path.join(self.base, "media", "boot_logo.png")
        
        if os.path.exists(self.boot_img_path):
            img = Image.open(self.boot_img_path).resize((450, 850), Image.Resampling.LANCZOS)
            self.boot_img = ImageTk.PhotoImage(img)
            tk.Label(self.root, image=self.boot_img, bg="black").place(relx=0.5, rely=0.5, anchor="center")
        else:
            tk.Label(self.root, text="YuixOS\n2026", fg="white", bg="black", font=("Arial", 30)).place(relx=0.5, rely=0.5, anchor="center")

        # 4 saniye sonra sistemi aç
        self.root.after(4000, self.finish)

    def finish(self):
        self.root.destroy()
        self.on_complete()

# --- 2. ANA SİSTEM (MASAÜSTÜ) ---
class YuixOS_Main:
    def __init__(self, root):
        self.root = root
        self.root.title("YuixOS")
        self.root.geometry("450x850")
        self.root.configure(bg="black")
        
        self.base = r"C:\Users\LBH-MUSTAFA\Desktop\YuixOS"
        self.apps_dir = os.path.join(self.base, "apps")
        self.wall_dir = os.path.join(self.base, "media", "wallpapers")

        self.apps_config = [
            ("Arama", "Arama", "arama"), ("Ayarlar", "Ayarlar", "ayarlar"),
            ("Galeri", "Galeri", "galeri"), ("Hava Durumu", "Hava durumu", "hava"),
            ("Kamera", "Kamera", "kamera"), ("Mesajlar", "Mesajlar", "mesajlar"),
            ("Notlar", "Notlar", "notlar"), ("Hesap Makinesi", "Hesap Makinesi", "hesap")
        ]

        self.canvas = tk.Canvas(self.root, width=450, height=775, highlightthickness=0, bd=0, bg="black")
        self.canvas.pack(fill="both", expand=True)

        self.nav_bar = tk.Frame(self.root, bg="black", height=75)
        self.nav_bar.pack(fill="x", side="bottom")

        self.setup_ui()
        self.setup_nav()

    def setup_ui(self):
        # Duvar kağıdı
        try:
            if os.path.exists(self.wall_dir):
                files = [f for f in os.listdir(self.wall_dir) if f.lower().endswith((".png", ".jpg"))]
                if files:
                    img = Image.open(os.path.join(self.wall_dir, files[0])).resize((450, 850), Image.Resampling.LANCZOS)
                    self.bg_img = ImageTk.PhotoImage(img)
                    self.canvas.create_image(0, 0, image=self.bg_img, anchor="nw")
        except: pass

        # Status Bar
        self.canvas.create_rectangle(0, 0, 450, 35, fill="black", outline="")
        self.canvas.create_text(50, 17, text=time.strftime("%H:%M"), fill="white", font=("Arial", 10, "bold"))
        
        # Wi-Fi Simge Tıklama (Ayarlar'ı açar)
        wifi = self.canvas.create_text(355, 17, text="📶", fill="white", font=("Arial", 12))
        self.canvas.tag_bind(wifi, "<Button-1>", lambda e: self.baslat("Ayarlar", "ayarlar", "Ayarlar"))
        self.canvas.create_text(400, 17, text="%100 ⚡", fill="white", font=("Arial", 9))

        # İkonlar
        sx, sy = 75, 150
        gx, gy = 100, 140
        for i, (name, folder, starter) in enumerate(self.apps_config):
            path = os.path.join(self.apps_dir, folder)
            icon = None
            if os.path.exists(path):
                for f in os.listdir(path):
                    if f.lower().endswith(".png"):
                        icon = os.path.join(path, f)
                        break
            
            px, py = sx + (i % 4) * gx, sy + (i // 4) * gy
            if icon:
                img = Image.open(icon).resize((70, 70), Image.Resampling.LANCZOS)
                img_tk = ImageTk.PhotoImage(img)
                btn = tk.Button(self.root, image=img_tk, bg="black", activebackground="#333", bd=0, 
                                highlightthickness=0, command=lambda f=folder, s=starter, n=name: self.baslat(f, s, n))
                btn.image = img_tk
                self.canvas.create_window(px, py, window=btn)
            self.canvas.create_text(px, py + 50, text=name, fill="white", font=("Arial", 9, "bold"), anchor="n")

    def setup_nav(self):
        # Geri (◁), Ana (◯), Klavye (⌨)
        tk.Button(self.nav_bar, text="◁", fg="white", bg="black", bd=0, font=("Arial", 24), command=lambda: print("Geri")).place(relx=0.2, rely=0.5, anchor="center")
        tk.Button(self.nav_bar, text="◯", fg="white", bg="black", bd=0, font=("Arial", 20), command=lambda: print("Home")).place(relx=0.5, rely=0.5, anchor="center")
        tk.Button(self.nav_bar, text="⌨", fg="white", bg="black", bd=0, font=("Arial", 18)).place(relx=0.8, rely=0.5, anchor="center")

    def baslat(self, folder, starter, name):
        full = os.path.join(self.apps_dir, folder)
        found = False
        if os.path.exists(full):
            for f in os.listdir(full):
                if f.lower().endswith(".py"):
                    subprocess.Popen(["python", f], cwd=full)
                    found = True
                    break
        if not found: messagebox.showerror("Hata", f"{name} bulunamadı!")

# --- ÇALIŞTIRICI ---
def main():
    boot_root = tk.Tk()
    def open_os():
        main_root = tk.Tk()
        YuixOS_Main(main_root)
        main_root.mainloop()
    YuixOS_Boot(boot_root, open_os)
    boot_root.mainloop()

if __name__ == "__main__":
    main()