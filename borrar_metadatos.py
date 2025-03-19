import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import piexif


def seleccionar_imagen():
    archivo = filedialog.askopenfilename(filetypes=[("Imágenes", "*.jpg;*.jpeg;*.png")])
    if archivo:
        entry_ruta.delete(0, tk.END)
        entry_ruta.insert(0, archivo)

def guardar_como():
    archivo = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png")])
    if archivo:
        entry_salida.delete(0, tk.END)
        entry_salida.insert(0, archivo)

def eliminar_metadatos():
    ruta_imagen = entry_ruta.get()
    ruta_salida = entry_salida.get().strip()
    
    if not ruta_imagen:
        messagebox.showerror("Error", "Por favor selecciona una imagen.")
        return

    if not ruta_salida:
        ruta_salida = ruta_imagen

    try:
        imagen = Image.open(ruta_imagen)
        imagen = imagen.convert("RGB")
        imagen.save(ruta_salida)
        messagebox.showinfo("Éxito", "Metadatos eliminados correctamente.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Crear ventana
ventana = tk.Tk()
ventana.title("Eliminador de Metadatos de Imágenes")
ventana.geometry("500x250")

# Elementos UI
label_ruta = tk.Label(ventana, text="Ruta de la imagen:")
label_ruta.pack(pady=5)
entry_ruta = tk.Entry(ventana, width=50)
entry_ruta.pack(pady=5)
btn_seleccionar = tk.Button(ventana, text="Seleccionar Imagen", command=seleccionar_imagen)
btn_seleccionar.pack(pady=5)

label_salida = tk.Label(ventana, text="Ruta de salida (opcional):")
label_salida.pack(pady=5)
entry_salida = tk.Entry(ventana, width=50)
entry_salida.pack(pady=5)
btn_guardar_como = tk.Button(ventana, text="Guardar Como", command=guardar_como)
btn_guardar_como.pack(pady=5)

btn_eliminar = tk.Button(ventana, text="Eliminar Metadatos", command=eliminar_metadatos)
btn_eliminar.pack(pady=20)

ventana.mainloop()
