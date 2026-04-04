import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import platform
import os
import subprocess
import time

animasyon_acik = True
koyu_tema = True
bagli_ag = None

def animasyon_efekti(widget, command):
    if animasyon_acik:
        original_color = widget.cget("bg")
        widget.config(bg="#555555")
        root.after(100, lambda: widget.config(bg=original_color))
        root.after(150, command)
    else:
        command()

def tema_degistir():
    global koyu_tema
    koyu_tema = tema_var.get()
    bg_color = "#121212" if koyu_tema else "#f0f0f0"
    fg_color = "white" if koyu_tema else "black"
    root.configure(bg=bg_color)
    label_sistem.config(bg=bg_color, fg=fg_color)

def parlaklik_ayar(val):
    try:
        brightness = int(float(val))
        os.system(f'powershell (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{brightness})')
    except:
        pass

def wifi_tara():
    global bagli_ag
    for widget in wifi_liste_frame.winfo_children():
        widget.destroy()
    try:
        current_status = subprocess.check_output(["netsh", "wlan", "show", "interfaces"]).decode("ascii", errors="ignore")
        for line in current_status.split("\n"):
            if " SSID" in line and ":" in line:
                bagli_ag = line.split(":")[1].strip()

        results = subprocess.check_output(["netsh", "wlan", "show", "networks"]).decode("ascii", errors="ignore")
        networks = []
        for line in results.split("\n"):
            if "SSID" in line:
                ssid = line.split(":")[1].strip()
                if ssid: networks.append(ssid)
        
        for ssid in set(networks):
            f = tk.Frame(wifi_liste_frame, bg="#222", pady=5)
            f.pack(fill="x", pady=2)
            lbl_text = f"📶 {ssid}"
            if ssid == bagli_ag:
                lbl_text += " (BAĞLI)"
            
            tk.Label(f, text=lbl_text, fg="white", bg="#222").pack(side="left", padx=10)
            btn = tk.Button(f, text="Yönet", bg="#444", fg="white")
            btn.config(command=lambda b=btn, s=ssid: animasyon_efekti(b, lambda: ag_yonet_pencere(s)))
            btn.pack(side="right", padx=10)
    except:
        tk.Label(wifi_liste_frame, text="Hata", fg="red", bg="#222").pack()

def ag_yonet_pencere(ssid):
    yonet_pencere = tk.Toplevel(root)
    yonet_pencere.geometry("500x400")
    yonet_pencere.configure(bg="#1c1c1c")
    tk.Label(yonet_pencere, text=ssid, fg="white", bg="#1c1c1c", font=("Arial", 14, "bold")).pack(pady=20)

    if ssid != bagli_ag:
        def gercek_baglan():
            sifre = simpledialog.askstring("Wi-Fi", f"{ssid} şifresi:", show='*')
            if sifre:
                profile_xml = f"""<?xml version="1.0"?>
<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
    <name>{ssid}</name>
    <SSIDConfig><SSID><name>{ssid}</name></SSID></SSIDConfig>
    <connectionType>ESS</connectionType>
    <connectionMode>auto</connectionMode>
    <MSM><security><authEncryption>
        <authentication>WPA2PSK</authentication>
        <encryption>AES</encryption>
        <useOneX>false</useOneX>
    </authEncryption><sharedKey>
        <keyType>passPhrase</keyType>
        <protected>false</protected>
        <keyMaterial>{sifre}</keyMaterial>
    </sharedKey></security></MSM>
</WLANProfile>"""
                with open("temp_wifi.xml", "w") as f: f.write(profile_xml)
                subprocess.run(["netsh", "wlan", "add", "profile", "filename=temp_wifi.xml"], shell=True)
                os.remove("temp_wifi.xml")
                subprocess.run(["netsh", "wlan", "connect", f"name={ssid}"], shell=True)
                time.sleep(2)
                wifi_tara()
                yonet_pencere.destroy()
        tk.Button(yonet_pencere, text="BAĞLAN", bg="#34C759", fg="white", width=20, command=gercek_baglan).pack(pady=5)
    else:
        def baglantiyi_kes():
            subprocess.run(["netsh", "wlan", "disconnect"], shell=True)
            wifi_tara()
            yonet_pencere.destroy()
        tk.Button(yonet_pencere, text="BAĞLANTIYI KES", bg="#FF9500", fg="white", width=20, command=baglantiyi_kes).pack(pady=5)

    def agi_unut():
        subprocess.run(["netsh", "wlan", "delete", "profile", f"name={ssid}"], shell=True)
        wifi_tara()
        yonet_pencere.destroy()
    tk.Button(yonet_pencere, text="AĞI UNUT", bg="#FF3B30", fg="white", width=20, command=agi_unut).pack(pady=5)

root = tk.Tk()
root.title("YuixOS Ayarlar")
root.geometry("900x1790")
root.configure(bg="#121212")

label_sistem = tk.Label(root, text="YuixOS Ayarlar", font=("Arial", 24, "bold"), fg="#555", bg="#121212")
label_sistem.pack(pady=20)

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

frame_apps = tk.Frame(notebook, bg="#1e1e1e")
notebook.add(frame_apps, text="Uygulamalar")
app_list = [("Mesajlar", "apps/Mesajlar/icon.png"), ("Saat", "apps/Saat/icon.png"), ("Telefon", "apps/Telefon/icon.png")]
for app_name, icon_path in app_list:
    f = tk.Frame(frame_apps, bg="#1e1e1e", pady=10)
    f.pack(fill="x", padx=20)
    try:
        img = tk.PhotoImage(file=icon_path).subsample(4, 4)
        lbl_img = tk.Label(f, image=img, bg="#1e1e1e")
        lbl_img.image = img
        lbl_img.pack(side="left", padx=5)
    except:
        tk.Label(f, text="📦", bg="#1e1e1e", fg="white", font=("Arial", 20)).pack(side="left", padx=5)
    tk.Label(f, text=app_name, fg="white", font=("Arial", 14), bg="#1e1e1e").pack(side="left", padx=10)
    btn_sil = tk.Button(f, text="SİL", bg="#ff4444", fg="white")
    btn_sil.config(command=lambda b=btn_sil, fr=f: animasyon_efekti(b, fr.destroy))
    btn_sil.pack(side="right")

frame_sys = tk.Frame(notebook, bg="#1e1e1e")
notebook.add(frame_sys, text="Sistem")
sys_info = f"OS: YuixOS\nİşlemci: {platform.processor()}\nRAM: 8GB\nHafıza: 256GB"
tk.Label(frame_sys, text=sys_info, fg="white", bg="#1e1e1e", font=("Arial", 14), justify="left").pack(pady=50)

frame_screen = tk.Frame(notebook, bg="#1e1e1e")
notebook.add(frame_screen, text="Ekran")
tema_var = tk.BooleanVar(value=True)
tk.Checkbutton(frame_screen, text="Koyu Tema", variable=tema_var, command=tema_degistir, bg="#1e1e1e").pack(pady=20)
tk.Scale(frame_screen, from_=0, to=100, orient="horizontal", label="Parlaklık", command=parlaklik_ayar, bg="#1e1e1e", fg="white").pack(fill="x", padx=50)

frame_wifi = tk.Frame(notebook, bg="#1e1e1e")
notebook.add(frame_wifi, text="Wi-Fi")
btn_scan = tk.Button(frame_wifi, text="TARA", bg="#007AFF", fg="white", command=lambda: animasyon_efekti(btn_scan, wifi_tara))
btn_scan.pack(pady=10)
wifi_liste_frame = tk.Frame(frame_wifi, bg="#222")
wifi_liste_frame.pack(fill="both", expand=True, padx=20)

frame_mobile = tk.Frame(notebook, bg="#1e1e1e")
notebook.add(frame_mobile, text="Mobil Veri")
tk.Button(frame_mobile, text="VERİ AÇ/KAPAT", bg="#34C759", fg="white").pack(pady=20)

frame_audio = tk.Frame(notebook, bg="#1e1e1e")
notebook.add(frame_audio, text="Ses")
tk.Scale(frame_audio, from_=0, to=100, orient="horizontal", label="Ses", bg="#1e1e1e", fg="white").pack(fill="x", padx=50, pady=50)

frame_anim = tk.Frame(notebook, bg="#1e1e1e")
notebook.add(frame_anim, text="Animasyon")
anim_var = tk.BooleanVar(value=True)
tk.Checkbutton(frame_anim, text="Aktif", variable=anim_var, command=lambda: globals().update(animasyon_acik=anim_var.get()), bg="#1e1e1e").pack(pady=20)

root.mainloop()