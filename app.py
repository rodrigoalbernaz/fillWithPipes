import pandas as pd
import tkinter as tk
from tkinter import simpledialog, filedialog

# Inicializar GUI
root = tk.Tk()
root.withdraw()

# Seleccionar archivo TXT
file_path = filedialog.askopenfilename(
    title="Selext TXT file",
    filetypes=[("Text files", "*.txt")]
)

if file_path:
    # Pedir datos al usuario
    settlement_currency = simpledialog.askstring("Input", "Enter Settlement Currency (e.g., USD):")
    exchange_rate = simpledialog.askfloat("Input", "Enter Settlement Exchange Rate (e.g., 4319.1616):")

    # Leer el archivo
    df = pd.read_csv(file_path, delimiter='|')

    # Completar los campos
    df['Settlement_Currency'] = settlement_currency
    df['Settlement_Exchange_Rate'] = exchange_rate
    df['Settlement_Amount'] = (df['Amount'] / exchange_rate).round(4)

    # Guardar archivo actualizado
    output_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt")],
        title="Save new file"
    )

    if output_path:
        df.to_csv(output_path, sep='|', index=False)
        print(f"✅ File succesfully saved:\n{output_path}")
    else:
        print("❌ No path selected to save file")
else:
    print("❌ No file selected")