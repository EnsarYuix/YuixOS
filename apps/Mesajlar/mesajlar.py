import tkinter as tk

root = tk.Tk()
root.title("KorfezOS Mesajlar")

root.geometry("900x1790")

root.configure(bg="#202020")

baslik = tk.Label(root, text="MESAJLAR", fg="white", bg="#202020", font=("Arial", 24, "bold"))
baslik.pack(pady=50)

mesaj_alani = tk.Label(root, text="Henüz mesaj yok...", fg="gray", bg="#202020", font=("Arial", 14))
mesaj_alani.pack(expand=True)

root.mainloop()