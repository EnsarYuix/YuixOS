import tkinter as tk
from tkinter import ttk
from datetime import datetime
import winsound
import random

kisiler = []
arama_gecmisi = []
konusma_saniye = 0
konusma_devam_ediyor = False

def guncelle_konusma_suresi(label_sure, label_durum):
    global konusma_saniye
    if konusma_devam_ediyor:
        label_durum.config(text="Bağlandı", fg="#00FFCC")
        konusma_saniye += 1
        dakika, saniye = divmod(konusma_saniye, 60)
        saat, dakika = divmod(dakika, 60)
        label_sure.config(text=f"{saat:02d}:{dakika:02d}:{saniye:02d}")
        root.after(1000, lambda: guncelle_konusma_suresi(label_sure, label_durum))

def arama_yap(kisi_ad):
    global konusma_devam_ediyor, konusma_saniye
    arama_ekrani = tk.Toplevel(root)
    arama_ekrani.geometry("900x1790")
    arama_ekrani.configure(bg="#1c1c1c")
    
    arama_gecmisi.insert(0, {"ad": kisi_ad, "zaman": datetime.now().strftime("%H:%M")})
    gecmis_listele()

    label_ust = tk.Label(arama_ekrani, text="YuixOS Arama", fg="#888", bg="#1c1c1c", font=("Arial", 18))
    label_ust.pack(pady=50)
    
    profil_frame = tk.Frame(arama_ekrani, width=250, height=250, bg="#333")
    profil_frame.pack(pady=40)
    tk.Label(profil_frame, text=kisi_ad[0].upper(), fg="white", bg="#333", font=("Arial", 80)).place(relx=0.5, rely=0.5, anchor="center")
    
    tk.Label(arama_ekrani, text=kisi_ad, fg="white", bg="#1c1c1c", font=("Arial", 35, "bold")).pack(pady=10)
    
    label_durum = tk.Label(arama_ekrani, text="Aranıyor...", fg="#FFD700", bg="#1c1c1c", font=("Arial", 20))
    label_durum.pack(pady=10)
    
    label_sure = tk.Label(arama_ekrani, text="00:00:00", fg="#1c1c1c", bg="#1c1c1c", font=("Arial", 25))
    label_sure.pack(pady=20)

    def cevapla():
        global konusma_devam_ediyor, konusma_saniye
        konusma_devam_ediyor = True
        konusma_saniye = 0
        label_sure.config(fg="#00FFCC")
        guncelle_konusma_suresi(label_sure, label_durum)

    def arama_sesi(tekrar=0):
        if not konusma_devam_ediyor and tekrar < 3:
            winsound.Beep(400, 1000)
            arama_ekrani.after(1000, lambda: arama_sesi(tekrar + 1))
        elif tekrar >= 3:
            cevapla()

    arama_sesi()

    def aramayi_kapat():
        global konusma_devam_ediyor
        konusma_devam_ediyor = False
        arama_ekrani.destroy()

    tk.Button(arama_ekrani, text="✕", command=aramayi_kapat, bg="#FF3B30", fg="white", font=("Arial", 40), width=3, bd=0).pack(side="bottom", pady=150)

def kisi_ekle_pencere():
    pencere = tk.Toplevel(root)
    pencere.geometry("700x900")
    pencere.configure(bg="#222")
    
    fields = ["Adı Soyadı", "Telefon", "E-posta"]
    entries = {}
    
    for field in fields:
        tk.Label(pencere, text=field, fg="#bbb", bg="#222", font=("Arial", 12)).pack(pady=(20,0))
        e = tk.Entry(pencere, font=("Arial", 16), width=30)
        e.pack(pady=10)
        entries[field] = e

    def kaydet():
        ad = entries["Adı Soyadı"].get()
        if ad:
            kisiler.append(ad)
            kisi_listele()
            pencere.destroy()

    tk.Button(pencere, text="KAYDET", command=kaydet, bg="#28a745", fg="white", font=("Arial", 14), width=20).pack(pady=40)

def kisi_listele():
    for widget in frame_kisi_liste.winfo_children():
        widget.destroy()
    for kisi in kisiler:
        f = tk.Frame(frame_kisi_liste, bg="#121212", pady=10)
        f.pack(fill="x")
        tk.Label(f, text=kisi, fg="white", bg="#121212", font=("Arial", 16)).pack(side="left", padx=20)
        tk.Button(f, text="Ara", command=lambda k=kisi: arama_yap(k), bg="#007AFF", fg="white", width=8).pack(side="right", padx=20)

def gecmis_listele():
    for widget in frame_gecmis_liste.winfo_children():
        widget.destroy()
    for g in arama_gecmisi:
        f = tk.Frame(frame_gecmis_liste, bg="#121212", pady=10)
        f.pack(fill="x")
        tk.Label(f, text=f"⬅ {g['ad']} ({g['zaman']})", fg="#ddd", bg="#121212", font=("Arial", 14)).pack(side="left", padx=20)

root = tk.Tk()
root.title("YuixOS Telefon")
root.geometry("900x1790")
root.configure(bg="#121212")

label_sistem = tk.Label(root, text="YuixOS", font=("Arial", 24, "bold"), fg="#555", bg="#121212")
label_sistem.pack(pady=20)

tk.Button(root, text="+ Kişi Ekle", command=kisi_ekle_pencere, bg="#34C759", fg="white", font=("Arial", 14, "bold"), padx=20).pack(pady=10)

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, pady=20)

frame_rehber = tk.Frame(notebook, bg="#121212")
notebook.add(frame_rehber, text="  📞 Aramalar  ")
frame_kisi_liste = tk.Frame(frame_rehber, bg="#121212")
frame_kisi_liste.pack(fill="both", expand=True)

frame_son = tk.Frame(notebook, bg="#121212")
notebook.add(frame_son, text="  🕒 Son Aramalar  ")
frame_gecmis_liste = tk.Frame(frame_son, bg="#121212")
frame_gecmis_liste.pack(fill="both", expand=True)

root.mainloop()