import tkinter as tk
from datetime import datetime
import random

class YuixHavaDurumu:
    def __init__(self, root):
        self.root = root
        self.root.title("YuixOS Hava Durumu")
        self.root.geometry("450x850")
        self.root.configure(bg="#1e272e")

        self.durumlar = ["Güneşli", "Bulutlu", "Yağmurlu", "Parçalı Bulutlu"]
        self.ikonlar = {"Güneşli": "☀️", "Bulutlu": "☁️", "Yağmurlu": "🌧️", "Parçalı Bulutlu": "⛅"}
        self.gunler = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]

        self.arayuz_olustur()

    def arayuz_olustur(self):
        tk.Label(self.root, text="KOCAELİ", fg="white", bg="#1e272e", font=("Arial", 22, "bold")).pack(pady=(40, 5))
        
        su_an_hava = random.choice(self.durumlar)
        tk.Label(self.root, text=self.ikonlar[su_an_hava], fg="#feca57", bg="#1e272e", font=("Arial", 70)).pack()
        tk.Label(self.root, text="24°C", fg="white", bg="#1e272e", font=("Arial", 50, "bold")).pack()
        tk.Label(self.root, text=su_an_hava, fg="#d2dae2", bg="#1e272e", font=("Arial", 14)).pack()

        saatlik_frame = tk.Frame(self.root, bg="#2f3542")
        saatlik_frame.pack(fill="x", padx=15, pady=20)
        
        canvas = tk.Canvas(saatlik_frame, bg="#2f3542", height=100, highlightthickness=0)
        scroll_x = tk.Frame(canvas, bg="#2f3542")
        canvas.pack(side="top", fill="x")

        saatler = ["12:00", "15:00", "18:00", "21:00", "00:00", "03:00", "06:00"]
        for s in saatler:
            f = tk.Frame(scroll_x, bg="#2f3542", padx=15)
            f.pack(side="left")
            tk.Label(f, text=s, fg="#d2dae2", bg="#2f3542", font=("Arial", 9)).pack()
            tk.Label(f, text=random.choice(list(self.ikonlar.values())), bg="#2f3542", font=("Arial", 15)).pack(pady=5)
            tk.Label(f, text=f"{random.randint(15,25)}°", fg="white", bg="#2f3542", font=("Arial", 10, "bold")).pack()
        
        canvas.create_window((0,0), window=scroll_x, anchor="nw")
        scroll_x.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        liste_frame = tk.Frame(self.root, bg="#1e272e")
        liste_frame.pack(fill="both", expand=True, padx=20)

        bugun = datetime.now().weekday()
        for i in range(7):
            idx = (bugun + i) % 7
            g_adi = self.gunler[idx]
            h_durum = random.choice(self.durumlar)
            
            satir = tk.Frame(liste_frame, bg="#1e272e", pady=8)
            satir.pack(fill="x")
            
            tk.Label(satir, text=g_adi, fg="white", bg="#1e272e", font=("Arial", 11), width=12, anchor="w").pack(side="left")
            tk.Label(satir, text=self.ikonlar[h_durum], bg="#1e272e", font=("Arial", 14)).pack(side="left", padx=30)
            tk.Label(satir, text=f"{random.randint(18,28)}°", fg="white", bg="#1e272e", font=("Arial", 11, "bold")).pack(side="right")

        tk.Button(self.root, text="🏠", font=("Arial", 18), fg="white", bg="#34495e", bd=0, 
                  command=self.root.destroy).pack(side="bottom", pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = YuixHavaDurumu(root)
    root.mainloop()