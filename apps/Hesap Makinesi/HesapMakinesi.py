import tkinter as tk
from tkinter import font

class YuixCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Hesap Makinesi")
        self.root.geometry("450x800")
        self.root.configure(bg="#000000")

        self.equation = ""
        
        # Ekran (Sonuç alanı)
        self.display_frame = tk.Frame(self.root, bg="#000000", height=200)
        self.display_frame.pack(fill="both", expand=True)

        self.label = tk.Label(self.display_frame, text="0", anchor="e", fg="white", 
                              bg="#000000", font=("Arial", 40))
        self.label.pack(fill="both", expand=True, padx=20, pady=40)

        # Butonlar Paneli
        self.buttons_frame = tk.Frame(self.root, bg="#000000")
        self.buttons_frame.pack(fill="both", expand=True, side="bottom", pady=20)

        self.create_buttons()

    def create_buttons(self):
        buttons = [
            ('C', '#A5A5A5', 'black'), ('±', '#A5A5A5', 'black'), ('%', '#A5A5A5', 'black'), ('/', '#FF9F0A', 'white'),
            ('7', '#333333', 'white'), ('8', '#333333', 'white'), ('9', '#333333', 'white'), ('*', '#FF9F0A', 'white'),
            ('4', '#333333', 'white'), ('5', '#333333', 'white'), ('6', '#333333', 'white'), ('-', '#FF9F0A', 'white'),
            ('1', '#333333', 'white'), ('2', '#333333', 'white'), ('3', '#333333', 'white'), ('+', '#FF9F0A', 'white'),
            ('0', '#333333', 'white'), ('.', '#333333', 'white'), ('=', '#FF9F0A', 'white')
        ]

        row = 0
        col = 0
        for btn_text, bg_color, fg_color in buttons:
            cmd = lambda x=btn_text: self.on_click(x)
            
            # Sıfır tuşu için özel genişlik
            if btn_text == '0':
                btn = tk.Button(self.buttons_frame, text=btn_text, width=10, height=2, 
                                bg=bg_color, fg=fg_color, font=("Arial", 18, "bold"),
                                bd=0, command=cmd)
                btn.grid(row=row, column=col, columnspan=2, sticky="nsew", padx=5, pady=5)
                col += 2
            else:
                btn = tk.Button(self.buttons_frame, text=btn_text, width=5, height=2, 
                                bg=bg_color, fg=fg_color, font=("Arial", 18, "bold"),
                                bd=0, command=cmd)
                btn.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
                col += 1

            if col > 3:
                col = 0
                row += 1

        for i in range(4):
            self.buttons_frame.grid_columnconfigure(i, weight=1)

    def on_click(self, char):
        if char == 'C':
            self.equation = ""
            self.label.config(text="0")
        elif char == '=':
            try:
                # Hesaplama yaparken '*' ve '/' işaretlerini kontrol et
                result = str(eval(self.equation.replace('x', '*').replace('÷', '/')))
                self.label.config(text=result)
                self.equation = result
            except:
                self.label.config(text="Hata")
                self.equation = ""
        else:
            self.equation += str(char)
            self.label.config(text=self.equation)

if __name__ == "__main__":
    root = tk.Tk()
    # Alt navigasyon barı için yer kalsın diye yüksekliği ayarladık
    app = YuixCalculator(root)
    root.mainloop()