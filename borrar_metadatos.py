import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import piexif
import PyPDF2
import mutagen
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.easyid3 import EasyID3
import docx
import subprocess
import os

def seleccionar_archivo():
    archivo = filedialog.askopenfilename(filetypes=[("Todos los archivos", "*.*")])
    if archivo:
        entry_ruta.delete(0, tk.END)
        entry_ruta.insert(0, archivo)

def guardar_como():
    archivo = filedialog.asksaveasfilename(defaultextension="", filetypes=[("Todos los archivos", "*.*")])
    if archivo:
        entry_salida.delete(0, tk.END)
        entry_salida.insert(0, archivo)

def eliminar_metadatos():
    ruta_archivo = entry_ruta.get()
    ruta_salida = entry_salida.get().strip()

    if not ruta_archivo:
        messagebox.showerror("Error", "Por favor selecciona un archivo.")
        return

    if not ruta_salida:
        ruta_salida = ruta_archivo

    try:
        if ruta_archivo.lower().endswith(('.jpg', '.jpeg')):
            eliminar_metadatos_imagen(ruta_archivo, ruta_salida)
        elif ruta_archivo.lower().endswith('.png'):
            eliminar_metadatos_png(ruta_archivo, ruta_salida)
        elif ruta_archivo.lower().endswith('.pdf'):
            eliminar_metadatos_pdf(ruta_archivo, ruta_salida)
        elif ruta_archivo.lower().endswith(('.mp3', '.flac')):
            eliminar_metadatos_audio(ruta_archivo)
        elif ruta_archivo.lower().endswith('.docx'):
            eliminar_metadatos_docx(ruta_archivo, ruta_salida)
        elif ruta_archivo.lower().endswith('.mp4'):
            eliminar_metadatos_video(ruta_archivo, ruta_salida)
        else:
            messagebox.showerror("Error", "Formato no soportado.")
            return

        messagebox.showinfo("Éxito", "Metadatos eliminados correctamente.")

    except Exception as e:
        messagebox.showerror("Error", str(e))

def eliminar_metadatos_imagen(entrada, salida):
    imagen = Image.open(entrada)
    imagen = imagen.convert("RGB")
    imagen.save(salida, "jpeg", quality=95)

def eliminar_metadatos_png(entrada, salida):
    imagen = Image.open(entrada)
    imagen.save(salida, "png")

def eliminar_metadatos_pdf(entrada, salida):
    with open(entrada, "rb") as archivo_pdf:
        lector_pdf = PyPDF2.PdfReader(archivo_pdf)
        escritor_pdf = PyPDF2.PdfWriter()
        for pagina in lector_pdf.pages:
            escritor_pdf.add_page(pagina)
        escritor_pdf.add_metadata({})
        with open(salida, "wb") as nuevo_pdf:
            escritor_pdf.write(nuevo_pdf)

def eliminar_metadatos_audio(entrada):
    if entrada.lower().endswith('.mp3'):
        audio = MP3(entrada, ID3=EasyID3)
    elif entrada.lower().endswith('.flac'):
        audio = FLAC(entrada)
    audio.delete()
    audio.save()

def eliminar_metadatos_docx(entrada, salida):
    doc = docx.Document(entrada)
    props = doc.core_properties
    props.author = ""
    props.title = ""
    props.subject = ""
    props.keywords = ""
    props.comments = ""
    doc.save(salida)

def eliminar_metadatos_video(entrada, salida):
    ruta_exiftool = r"C:\ExifTool\exiftool.exe"  # Ruta completa al ejecutable
    if not os.path.isfile(ruta_exiftool):
        raise FileNotFoundError("ExifTool no se encontró. Verifica la ruta.")
    
    comando = [
        ruta_exiftool,
        "-all=",
        "-o", salida,
        entrada
    ]
    subprocess.run(comando, shell=True, check=True)

# Crear ventana
ventana = tk.Tk()
ventana.title("Eliminador de Metadatos")
ventana.geometry("500x250")

# Elementos UI
label_ruta = tk.Label(ventana, text="Ruta del archivo:")
label_ruta.pack(pady=5)
entry_ruta = tk.Entry(ventana, width=50)
entry_ruta.pack(pady=5)
btn_seleccionar = tk.Button(ventana, text="Seleccionar Archivo", command=seleccionar_archivo)
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
