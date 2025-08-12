import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import qrcode
from PIL import Image, ImageTk


class QRGeneratorApp:
    def __init__(self, master):
        self.master = master
        master.title("Gerador de QR Code")
        master.geometry("520x680")
        master.resizable(True, True)

        # ----- Frame de entrada -----
        frm = ttk.Frame(master, padding=12)
        frm.pack(fill="x", padx=8, pady=6)

        ttk.Label(frm, text="Texto / URL:").grid(column=0, row=0, sticky="w")
        self.entry_text = ttk.Entry(frm, width=50)
        self.entry_text.grid(column=0, row=1, columnspan=3, pady=6, sticky="w")

        ttk.Label(frm, text="Tamanho (pixels por módulo):").grid(column=0, row=2, sticky="w", pady=(8, 0))
        self.scale_size = ttk.Scale(frm, from_=1, to=20, orient="horizontal")
        self.scale_size.set(8)
        self.scale_size.grid(column=0, row=3, sticky="we", columnspan=2)

        ttk.Label(frm, text="Borda (módulos):").grid(column=2, row=2, sticky="w", pady=(8, 0))
        self.spin_border = ttk.Spinbox(frm, from_=0, to=10, width=5)
        self.spin_border.set(4)
        self.spin_border.grid(column=2, row=3, sticky="w")

        # Opções de cor
        ttk.Label(frm, text="Cor do QR:").grid(column=0, row=4, sticky="w", pady=(10, 0))
        self.entry_fg = ttk.Entry(frm, width=12)
        self.entry_fg.insert(0, "#000000")
        self.entry_fg.grid(column=0, row=5, sticky="w")
        ttk.Label(frm, text="Fundo:").grid(column=1, row=4, sticky="w", pady=(10, 0))
        self.entry_bg = ttk.Entry(frm, width=12)
        self.entry_bg.insert(0, "#ffffff")
        self.entry_bg.grid(column=1, row=5, sticky="w")

        # Botões
        btn_frame = ttk.Frame(frm)
        btn_frame.grid(column=0, row=6, columnspan=3, pady=12, sticky="w")
        self.btn_generate = ttk.Button(btn_frame, text="Gerar QR", command=self.gerar_qr)
        self.btn_generate.grid(column=0, row=0, padx=(0, 8))
        self.btn_save = ttk.Button(btn_frame, text="Salvar imagem", command=self.salvar_imagem, state="disabled")
        self.btn_save.grid(column=1, row=0)

        # ----- Área de preview -----
        preview_frame = ttk.LabelFrame(master, text="Preview", padding=8)
        preview_frame.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        self.canvas = tk.Canvas(preview_frame, width=400, height=300, bg="#eee", highlightthickness=0)
        self.canvas.pack(expand=True, padx=8, pady=8)
        self.preview_image = None
        self.generated_img = None  # PIL Image guardada ao gerar

    def gerar_qr(self):
        texto = self.entry_text.get().strip()
        if not texto:
            messagebox.showwarning("Atenção", "Digite um texto ou URL para gerar o QR Code.")
            return

        try:
            box_size = int(float(self.scale_size.get()))
            border = int(self.spin_border.get())
            fg_color = self.entry_fg.get().strip() or "#000000"
            bg_color = self.entry_bg.get().strip() or "#ffffff"
        except Exception:
            messagebox.showerror("Erro", "Valores de tamanho/borda inválidos.")
            return

        # Cria o QR
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=box_size,
            border=border,
        )
        qr.add_data(texto)
        qr.make(fit=True)
        img = qr.make_image(fill_color=fg_color, back_color=bg_color).convert("RGBA")

        # Redimensiona para caber no canvas mantendo proporção máxima
        max_w, max_h = 400, 300
        w, h = img.size
        scale = min(max_w / w, max_h / h, 1)
        new_size = (int(w * scale), int(h * scale))
        img_resized = img.resize(new_size, Image.NEAREST)

        # Mantém referência para salvar depois
        self.generated_img = img

        # Converte para PhotoImage e mostra no canvas
        self.preview_image = ImageTk.PhotoImage(img_resized)
        self.canvas.delete("all")
        x = (max_w - new_size[0]) // 2
        y = (max_h - new_size[1]) // 2
        self.canvas.create_image(x, y, anchor="nw", image=self.preview_image)

        # habilita salvar
        self.btn_save.config(state="normal")

    def salvar_imagem(self):
        if self.generated_img is None:
            messagebox.showwarning("Aviso", "Gere um QR Code antes de salvar.")
            return

        fpath = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png"), ("All files", "*.*")],
            title="Salvar QR Code"
        )
        if not fpath:
            return

        try:
            # Salva o PIL Image original (em tamanho nativo)
            self.generated_img.save(fpath)
            messagebox.showinfo("Salvo", f"Imagem salva em:\n{fpath}")
        except Exception as e:
            messagebox.showerror("Erro ao salvar", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style(root)
    # Setar o tema
    try:
        style.theme_use('clam')
    except:
        pass
    app = QRGeneratorApp(root)
    root.mainloop()
