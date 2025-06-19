import cv2
import easyocr
import sqlite3
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import re

# ======= CONFIGURAÇÃO GLOBAL =======
DB_PATH = 'veiculos.db'
PLACA_REGEX = re.compile(r'^[A-Z]{3}[0-9][A-Z0-9][0-9]{2}$')
OCR_LANGUAGES = ['pt']

# ======= CONEXÃO COM BANCO =======
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# ======= OCR =======
reader = easyocr.Reader(OCR_LANGUAGES)

# ======= VARIÁVEIS =======
placa_detectada = ""

# ======= FUNÇÕES =======

def abrir_camera():
    """Abre a câmera e captura o frame ao pressionar 'c'."""
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        messagebox.showerror("Erro", "Não foi possível acessar a câmera.")
        return

    messagebox.showinfo("Info", "Pressione 'c' na janela da câmera para capturar, 'q' para cancelar.")

    while True:
        ret, frame = cap.read()
        if not ret:
            messagebox.showerror("Erro", "Erro ao capturar imagem da câmera.")
            break

        cv2.imshow("Posicione a placa e pressione 'c' para capturar", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('c'):
            cap.release()
            cv2.destroyAllWindows()
            processar_frame(frame)
            break
        elif key == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break


def processar_frame(frame):
    """Processa o frame capturado, executa OCR e exibe resultado."""
    global placa_detectada

    # Pré-processamento
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.bilateralFilter(gray, 11, 17, 17)

    # Exibir no painel
    exibir_imagem(frame)

    # OCR
    results = reader.readtext(blur)

    placa_detectada = ""
    for _, text, _ in results:
        text_clean = text.replace(" ", "").replace("-", "").upper()
        if PLACA_REGEX.match(text_clean):
            placa_detectada = text_clean
            break

    if placa_detectada:
        lbl_placa.config(text=f"Placa detectada: {placa_detectada}")
        botoes_confirmar.pack(pady=5)
    else:
        lbl_placa.config(text="Nenhuma placa válida detectada.")
        botoes_confirmar.pack_forget()


def exibir_imagem(frame):
    """Exibe o frame na interface Tkinter."""
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(frame_rgb).resize((600, 400))
    img_tk = ImageTk.PhotoImage(img_pil)
    panel.configure(image=img_tk)
    panel.image = img_tk


def confirmar_consulta():
    """Consulta a placa detectada no banco e exibe o resultado."""
    cursor.execute("SELECT * FROM veiculos WHERE placa = ?", (placa_detectada,))
    dados = cursor.fetchone()

    if dados:
        resultado = f"Placa: {dados[0]}\nDono: {dados[1]}\nSituação: {dados[2]}"
    else:
        resultado = "Veículo não encontrado na base de dados."

    messagebox.showinfo("Resultado", resultado)


def tentar_novamente():
    """Permite nova tentativa de captura."""
    lbl_placa.config(text="")
    botoes_confirmar.pack_forget()


def cancelar():
    """Cancela a consulta atual."""
    lbl_placa.config(text="")
    botoes_confirmar.pack_forget()


def sair():
    """Encerra o programa com segurança."""
    conn.close()
    root.destroy()


# ======= INTERFACE =======

root = tk.Tk()
root.title("Leitor de Placas - Tkinter")
root.geometry("900x700")

btn_capturar = tk.Button(
    root, text="Abrir Câmera", command=abrir_camera,
    font=("Arial", 16), bg="blue", fg="white"
)
btn_capturar.pack(pady=10)

panel = tk.Label(root)
panel.pack()

lbl_placa = tk.Label(root, text="", font=("Arial", 16))
lbl_placa.pack(pady=10)

botoes_confirmar = tk.Frame(root)
tk.Button(
    botoes_confirmar, text="Confirmar Consulta", command=confirmar_consulta,
    font=("Arial", 14), bg="green", fg="white"
).pack(side="left", padx=5)

tk.Button(
    botoes_confirmar, text="Tentar Novamente", command=tentar_novamente,
    font=("Arial", 14), bg="orange", fg="white"
).pack(side="left", padx=5)

tk.Button(
    botoes_confirmar, text="Cancelar", command=cancelar,
    font=("Arial", 14), bg="red", fg="white"
).pack(side="left", padx=5)

btn_sair = tk.Button(root, text="Sair", command=sair, font=("Arial", 14))
btn_sair.pack(pady=10)

root.mainloop()
