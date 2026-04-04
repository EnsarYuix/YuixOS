import tkinter as tk
from tkinter import ttk
import time
from datetime import datetime
import winsound

krono_calisiyor = False
krono_saniye = 0
kurulu_alarmlar = []

def guncelle_zaman():
    simdi = datetime.now()
    saat_yazisi = simdi.strftime("%H:%M:%S")
    tarih_yazisi = simdi.strftime("%d %B %Y %A")
    label_saat.config(text=saat_yazisi)
    label_tarih.config(text=tarih_yazisi)
    
    su_an = simdi.strftime("%H:%M")
    if su_an in kurulu_alarmlar:
        winsound.Beep(1000, 500)
        
    root.after(1000, guncelle_zaman)

def alarm_ekle():
    saat = alarm_entry.get()
    if saat and saat not in kurulu_alarmlar:
        kurulu_alarmlar.append(saat)
        frame = tk.Frame(liste_kaydirma_ic, bg="#1e1e1e", pady=5)
        frame.pack(fill="x")
        lbl = tk.Label(frame, text=f"⏰ {saat}", fg="white", bg="#1e1e1e", font=("Arial", 14))
        lbl.pack(side="left", padx=10)
        
        def sil():
            if saat in kurulu_alarmlar:
                kurulu_alarmlar.remove(saat)
            frame.destroy()
            
        btn = tk.Button(frame, text="Sil", command=sil, bg="#ff4444", fg="white")
        btn.pack(side="right", padx=10)

def krono_guncelle():
    global krono_saniye
    if krono_calisiyor:
        krono_saniye += 1
        dakika, saniye = divmod(krono_saniye, 60)
        saat, dakika = divmod(dakika, 60)
        label_krono.config(text=f"{saat:02d}:{dakika:02d}:{saniye:02d}")
        root.after(1000, krono_guncelle)

def krono_baslat():
    global krono_calisiyor
    if not krono_calisiyor:
        krono_calisiyor = True
        krono_guncelle()

def krono_durdur():
    global krono_calisiyor
    krono_calisiyor = False

def krono_sifirla():
    global krono_saniye, krono_calisiyor
    krono_calisiyor = False
    krono_saniye = 0
    label_krono.config(text="00:00:00")

root = tk.Tk()
root.title("YuixOS - Saat")
root.geometry("900x1790")
root.configure(bg="#121212")

label_sistem = tk.Label(root, text="YuixOS", font=("Arial", 24, "bold"), fg="#555", bg="#121212")
label_sistem.pack(pady=20)

label_saat = tk.Label(root, text="", font=("Arial", 80, "bold"), fg="#00FFCC", bg="#121212")
label_saat.pack(pady=(100, 10))

label_tarih = tk.Label(root, text="", font=("Arial", 20), fg="white", bg="#121212")
label_tarih.pack()

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, pady=50)

frame_alarm = tk.Frame(notebook, bg="#1e1e1e")
notebook.add(frame_alarm, text=" ⏰ Alarm ")

alarm_entry = tk.Entry(frame_alarm, font=("Arial", 30), width=8, justify="center")
alarm_entry.insert(0, "08:00")
alarm_entry.pack(pady=20)

tk.Button(frame_alarm, text="ALARM EKLE", command=alarm_ekle, bg="#00FFCC", font=("Arial", 12, "bold")).pack(pady=10)

liste_canvas = tk.Canvas(frame_alarm, bg="#1e1e1e", highlightthickness=0)
liste_canvas.pack(fill="both", expand=True, padx=20)
liste_kaydirma_ic = tk.Frame(liste_canvas, bg="#1e1e1e")
liste_canvas.create_window((0, 0), window=liste_kaydirma_ic, anchor="nw")

frame_krono = tk.Frame(notebook, bg="#1e1e1e")
notebook.add(frame_krono, text=" ⏱️ Kronometre ")

label_krono = tk.Label(frame_krono, text="00:00:00", fg="#00FFCC", bg="#1e1e1e", font=("Arial", 50, "bold"))
label_krono.pack(pady=100)

btn_frame = tk.Frame(frame_krono, bg="#1e1e1e")
btn_frame.pack()

tk.Button(btn_frame, text="BAŞLAT", command=krono_baslat, bg="green", fg="white", width=10).pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text="DURDUR", command=krono_durdur, bg="red", fg="white", width=10).pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text="SIFIRLA", command=krono_sifirla, bg="gray", fg="white", width=10).pack(side=tk.LEFT, padx=5)

guncelle_zaman()
root.mainloop()