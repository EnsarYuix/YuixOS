import tkinter as tk
from tkinter import messagebox, simpledialog
import os

class YuixNotlar:
    def __init__(self, root):
        self.root = root
        self.root.title("YuixOS Notlar")
        self.root.geometry("450x850")
        self.root.configure(bg="#0f0f0f")

        # Notların yolu (Masaüstündeki YuixOS klasörünün içinde 'notlar_verisi' açar)
        # Eğer klasör yoksa oluşturur
        self.not_yolu = os.path.join("..", "..", "notlar_verisi")
        if not os.path.exists(self.not_yolu):
            try:
                os.makedirs(self.not_yolu)
            except:
                # Eğer üst klasöre çıkamazsa direkt yanına oluşturur
                self.not_yolu = "notlar_verisi"
                if not os.path.exists(self.not_yolu): os.makedirs(self.not_yolu)

        # Üst Bar
        self.ust_bar = tk.Frame(self.root, bg="#1a1a1a", height=70)
        self.ust_bar.pack(fill="x")
        self.ust_bar.pack_propagate(False)
        tk.Label(self.ust_bar, text="NOTLARIM", fg="white", bg="#1a1a1a", font=("Arial", 14, "bold")).pack(side="left", padx=20)

        # Ana Liste Alanı (Kaydırma çubuğu eklendi)
        self.liste_frame = tk.Frame(self.root, bg="#0f0f0f")
        self.liste_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Alt Ekleme Butonu (+)
        self.ekle_btn = tk.Button(self.root, text="+", font=("Arial", 30), fg="white", bg="#2980b9", 
                                  activebackground="#3498db", bd=0, width=2, command=self.yeni_not_ekrani)
        self.ekle_btn.place(relx=0.85, rely=0.92, anchor="center")

        self.notlari_yukle()

    def notlari_yukle(self):
        # Ekranı temizle
        for w in self.liste_frame.winfo_children(): w.destroy()
        
        if not os.path.exists(self.not_yolu): return

        dosyalar = [f for f in os.listdir(self.not_yolu) if f.endswith(".txt")]
        
        if not dosyalar:
            tk.Label(self.liste_frame, text="Henüz not yok.\n'+' basarak başla!", fg="#555", bg="#0f0f0f", font=("Arial", 12)).pack(pady=100)
        
        for dosya in dosyalar:
            # Dosya ismini temiz göster
            gosterilecek_isim = dosya.replace(".txt", "")
            btn = tk.Button(self.liste_frame, text=f"📄 {gosterilecek_isim}", fg="white", bg="#222", 
                            font=("Arial", 11), anchor="w", padx=15, pady=10, bd=0, cursor="hand2",
                            command=lambda d=dosya: self.not_oku_duzenle(d))
            btn.pack(fill="x", pady=2)

    def yeni_not_ekrani(self):
        self.not_penceresi()

    def not_penceresi(self, eski_dosya=None, icerik=""):
        top = tk.Toplevel(self.root)
        top.title("Not Yazılıyor...")
        top.geometry("450x850")
        top.configure(bg="#1a1a1a")

        yazi_alani = tk.Text(top, bg="#1a1a1a", fg="white", font=("Arial", 12), padx=15, pady=15, bd=0, insertbackground="white")
        yazi_alani.insert("1.0", icerik)
        yazi_alani.pack(fill="both", expand=True)

        alt_bar = tk.Frame(top, bg="#111", height=80)
        alt_bar.pack(fill="x", side="bottom")

        def kaydet():
            yeni_icerik = yazi_alani.get("1.0", "end-1c")
            if not yeni_icerik.strip():
                messagebox.showwarning("YuixOS", "Boş not kaydedilemez!")
                return

            isim = simpledialog.askstring("YuixOS", "Not ismi ne olsun?", parent=top)
            if isim:
                # İsim boş değilse kaydet
                dosya_adi = f"{isim}.txt"
                tam_yol = os.path.join(self.not_yolu, dosya_adi)
                
                try:
                    # Eğer düzenleme yapılıyorsa ve isim değişmişse eskiyi sil
                    if eski_dosya and eski_dosya != dosya_adi:
                        os.remove(os.path.join(self.not_yolu, eski_dosya))
                    
                    with open(tam_yol, "w", encoding="utf-8") as f:
                        f.write(yeni_icerik)
                    
                    top.destroy()
                    self.notlari_yukle() # Listeyi tazele
                except Exception as e:
                    messagebox.showerror("Hata", f"Kaydedilemedi: {e}")

        def sil():
            if eski_dosya and messagebox.askyesno("YuixOS", "Bu not silinsin mi?"):
                os.remove(os.path.join(self.not_yolu, eski_dosya))
                top.destroy()
                self.notlari_yukle()

        tk.Button(alt_bar, text="💾 KAYDET", fg="white", bg="#27ae60", font=("Arial", 10, "bold"), bd=0, command=kaydet).pack(side="left", expand=True, fill="both")
        if eski_dosya:
            tk.Button(alt_bar, text="🗑️ SİL", fg="white", bg="#c0392b", font=("Arial", 10, "bold"), bd=0, command=sil).pack(side="left", expand=True, fill="both")

    def not_oku_duzenle(self, dosya):
        try:
            with open(os.path.join(self.not_yolu, dosya), "r", encoding="utf-8") as f:
                icerik = f.read()
            self.not_penceresi(eski_dosya=dosya, icerik=icerik)
        except Exception as e:
            messagebox.showerror("Hata", "Not açılamadı!")

if __name__ == "__main__":
    root = tk.Tk()
    app = YuixNotlar(root)
    root.mainloop()