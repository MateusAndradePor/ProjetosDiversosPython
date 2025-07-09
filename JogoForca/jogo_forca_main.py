import tkinter as tk
import random

# Lista de palavras:
def carregar_palavras():
    try:
        with open("data/palavras.txt", "r", encoding="utf-8") as arquivo:
            return [linha.strip().lower() for linha in arquivo if linha.strip()]
    except FileNotFoundError:
        print("Arquivo 'palavras.txt' não encontrado.")
        return ["janela"]  # palavra padrão

class JogoForca:
    # Definição da interface e campos do jogo:
    def __init__(self, master):
        self.master = master
        self.master.title("Jogo da Forca")
        self.master.geometry("400x300")
        self.master.resizable(False, False)

        self.palavra = ""
        self.letras_descobertas = []
        self.letras_erradas = []
        self.tentativas_restantes = 6

        self.label_palavra = tk.Label(master, text="", font=("Courier", 24))
        self.label_palavra.pack(pady=20)

        self.label_info = tk.Label(master, text="Digite uma letra:", font=("Arial", 12))
        self.label_info.pack()

        self.entrada_letra = tk.Entry(master, font=("Arial", 14), width=5, justify="center")
        self.entrada_letra.pack()

        self.botao_enviar = tk.Button(master, text="Chutar", command=self.verificar_letra)
        self.botao_enviar.pack(pady=5)

        self.label_status = tk.Label(master, text="", font=("Arial", 12))
        self.label_status.pack()

        self.label_erros = tk.Label(master, text="Erros: ", font=("Arial", 10))
        self.label_erros.pack(pady=10)

        self.botao_reiniciar = tk.Button(master, text="Novo Jogo", command=self.iniciar_jogo)
        self.botao_reiniciar.pack(pady=5)

        self.iniciar_jogo()

    # Inicia o jogo com a palavra aleatória:
    def iniciar_jogo(self):
        self.palavra = random.choice(carregar_palavras())
        self.letras_descobertas = ["_" for _ in self.palavra]
        self.letras_erradas = []
        self.tentativas_restantes = 6
        self.atualizar_interface("")
        self.label_status.config(text="")
        self.label_erros.config(text="Erros: ")

    # Verifica letras erradas:
    def verificar_letra(self):
        letra = self.entrada_letra.get().lower()
        self.entrada_letra.delete(0, tk.END)

        if not letra.isalpha() or len(letra) != 1:
            self.label_status.config(text="Digite uma única letra válida.")
            return

        if letra in self.letras_descobertas or letra in self.letras_erradas:
            self.label_status.config(text="Você já tentou essa letra.")
            return

        if letra in self.palavra:
            for i, l in enumerate(self.palavra):
                if l == letra:
                    self.letras_descobertas[i] = letra
            self.label_status.config(text="Acertou!")
        else:
            self.letras_erradas.append(letra)
            self.tentativas_restantes -= 1
            self.label_status.config(text=f"Errou! Tentativas restantes: {self.tentativas_restantes}")

        self.atualizar_interface(letra)

        if "_" not in self.letras_descobertas:
            self.label_status.config(text="Parabéns! Você venceu!")
        elif self.tentativas_restantes == 0:
            self.label_status.config(text=f"Você perdeu! A palavra era: {self.palavra}")

    def atualizar_interface(self, letra):
        self.label_palavra.config(text=" ".join(self.letras_descobertas))
        self.label_erros.config(text="Erros: " + ", ".join(self.letras_erradas))

# Execução
if __name__ == "__main__":
    root = tk.Tk()
    app = JogoForca(root)
    root.mainloop()
