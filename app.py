import tkinter as tk
from tkinter import filedialog, messagebox
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from PyPDF2 import PdfReader, PdfWriter
import os
import io
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
pdfmetrics.registerFont(TTFont('Montserrat', 'ofont.ru_Montserrat.ttf'))
def insert_text_to_pdf(input_pdf_path, output_pdf_path, text_data, text_color):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    for text_item in text_data:
        x, y, text = text_item['x'], text_item['y'], text_item['text']
        print(f"Inserting text '{text}' at coordinates ({x}, {y})")
        can.setFont('Montserrat', 16)
        if text_color == "black":
            can.setFillColorRGB(0, 0, 0)
        else:
            can.setFillColorRGB(255, 255, 255)
        can.drawString(x, A4[1] - y, text)
    can.save()
    packet.seek(0)
    new_pdf = PdfReader(packet)
    existing_pdf = PdfReader(open(input_pdf_path, "rb"))
    output = PdfWriter()
    for i in range(len(existing_pdf.pages)):
        page = existing_pdf.pages[i]
        if i < len(new_pdf.pages):
            page.merge_page(new_pdf.pages[i])
        output.add_page(page)
    with open(output_pdf_path, "wb") as outputStream:
        output.write(outputStream)
def process_pdfs(pdf_file, fio_list, x, y, text_color):
    base_dir = os.path.dirname(pdf_file)
    filename = os.path.basename(pdf_file).split('.')[0]
    fio_list = [fio.strip() for fio in fio_list.split(',')]

    for idx, fio in enumerate(fio_list):
        surname = fio.split()[0]
        output_pdf_path = os.path.join(base_dir, f"{filename}_{surname}_output_{idx + 1}.pdf")
        text_data = [{'x': x, 'y': y, 'text': fio}]
        insert_text_to_pdf(pdf_file, output_pdf_path, text_data, text_color)
        print(f"Saved {output_pdf_path}")
def select_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        entry_pdf.delete(0, tk.END)
        entry_pdf.insert(0, file_path)
def process_files():
    pdf_file = entry_pdf.get()
    fio_list = entry_fio.get()
    x = 130
    y = 639
    if not pdf_file or not fio_list:
        messagebox.showerror("Ошибка", "Выберите PDF файл и введите ФИО через запятую.")
        return
    if var_black.get():
        text_color = "black"
    elif var_white.get():
        text_color = "white"
    else:
        messagebox.showerror("Ошибка", "Выберите цвет текста.")
        return
    try:
        process_pdfs(pdf_file, fio_list, x, y, text_color)
        messagebox.showinfo("Успех", "Файлы успешно обработаны!")
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))
root = tk.Tk()
root.title("Обработка PDF")
label_pdf = tk.Label(root, text="Выберите PDF файл:")
label_pdf.grid(row=0, column=0, padx=10, pady=5)
entry_pdf = tk.Entry(root, width=50)
entry_pdf.grid(row=0, column=1, padx=10, pady=5)
button_browse = tk.Button(root, text="Обзор...", command=select_pdf)
button_browse.grid(row=0, column=2, padx=10, pady=5)
label_fio = tk.Label(root, text="Введите ФИО через запятую:")
label_fio.grid(row=1, column=0, padx=10, pady=5)
entry_fio = tk.Entry(root, width=50)
entry_fio.grid(row=1, column=1, padx=10, pady=5)
var_black = tk.BooleanVar()
var_white = tk.BooleanVar()
checkbox_black = tk.Checkbutton(root, text="Черный текст (Бородин)", variable=var_black)
checkbox_black.grid(row=4, column=0)
checkbox_white = tk.Checkbutton(root, text="Белый текст (Базаров)", variable=var_white)
checkbox_white.grid(row=4, column=1)
button_process = tk.Button(root, text="Обработать", command=process_files)
button_process.grid(row=5, column=0, columnspan=3, pady=10)
root.mainloop()
