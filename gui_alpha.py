import os
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from functions_alpha import *
from write_alpha import *

# region Variables
# global list_var
button_list_mode = []
button_list_file = []
dict_idiomas = {1: "español", 2: "inglés", 3: "francés", 4: "italiano", 5: "portugués", 6: "ruso", 7: "alemán",
                8: "chino", 9: "japonés"}
dict_trans = {"español": "es", "inglés": "en", "francés": "fr", "italiano": "it", "portugués": "pt", "ruso": "ru",
              "alemán": "de", "chino": "zh-cn", "japonés": "ja"}
dict_spacy = {"español": "es_core_news_sm", "inglés": "en_core_web_sm", "francés": "fr_core_news_sm",
              "italiano": "it_core_news_sm", "portugués": "pt_core_news_sm", "ruso": "ru_core_news_sm",
              "alemán": "de_core_news_sm", "chino": "zh_core_web_sm", "japonés": "ja_core_news_sm"}
reverse_dict = {_: __ for __, _ in dict_idiomas.items()}
# endregion


# region Commands
def instr():
    win2 = Tk()
    win2.title("Instrucciones")
    length = "1000"
    win2.geometry(f"{length}x650")
    try:
        with open("Instrucciones.txt", "r", encoding="utf-8") as _:
            file_inst = _.read()
    except FileNotFoundError:
        messagebox.showerror("Error de archivo", "No se encuentra el archivo de instrucciones. Favor de descargar")
        return
    except Exception as e:
        messagebox.showerror("Error de archivo", f"Ocurrió un error {e}")
        return
    lab_2 = Label(win2, text=file_inst, justify=LEFT, wraplength=int(length), anchor="w", font=("Arial", 14))
    lab_2.pack()


def desbloquear():
    if button_iniciar["state"] == "disabled":
        button_iniciar.config(state="normal")
        button_bloquear.config(text="Bloquear")
    else:
        button_iniciar.config(state="disabled")
        button_bloquear.config(text="Desbloquear")


def select(foo_btn, foo_list):
    foo_btn.config(relief="sunken", state="disabled")
    for _ in range(len(foo_list)):
        if foo_list[_] != foo_btn:
            foo_list[_].config(relief="raised", state="normal")


def inicio_check():

    def button_error():
        button_iniciar.config(state="disabled")
        button_bloquear.config(text="Desbloquear")

    list_var = []
    for _ in range(len(button_list_mode)):
        if button_list_mode[_]["relief"] == "sunken":
            list_var.append(_)
            break
        if _ == len(button_list_mode)-1:
            messagebox.showinfo("Seleccionar botón", "Favor de seleccionar un botón de modo antes de iniciar")
            button_error()
            return
    for _ in range(len(button_list_file)):
        if button_list_file[_]["relief"] == "sunken":
            list_var.append(_)
            break
        if _ == len(button_list_file)-1:
            messagebox.showinfo("Seleccionar botón",
                                "Favor de seleccionar un botón de tipo de archivo antes de iniciar.")
            button_error()
            return
    list_var.extend([entry_archivo.get(), entry_original.get(), entry_destino.get(), entry_name.get()])
    list_var.extend([combobox_source.get(), combobox_exit.get()])
    if list_var[2] == "" or list_var[3] == "" or list_var[4] == "" or list_var[5] == "":
        messagebox.showinfo("Ingresar idioma", "Favor de ingresar todos los bancos.")
        button_error()
        return
    if list_var[6] == "" or list_var[7] == "":
        messagebox.showinfo("Ingresar idioma", "Favor de seleccionar un idioma de origen o de traducción.")
        button_error()
        return
    if list_var[6] == list_var[7]:
        messagebox.showinfo("Mismo idioma", "Favor de seleccionar diferentes idiomas de origen y destino.")
        button_error()
        return
    name_foo, extension_foo = os.path.splitext(list_var[3])
    if extension_foo == "":
        list_var[3] += ".pdf"
    elif not extension_foo == ".pdf":
        messagebox.showinfo("Tipo incorrecto", "Favor de sólo seleccionar archivos PDF.")
        button_error()
        return
    name_original = os.path.join(list_var[2], list_var[3]).replace("\\", "/")
    if not os.path.exists(name_original):
        messagebox.showinfo("Dirección incorrecta", "Favor de escribir una dirección o un archivo existentes.")
        button_error()
        return
    if not os.path.exists(list_var[4]):
        messagebox.showinfo("Dirección incorrecta", "Favor de escribir una dirección de destino existente.")
        button_error()
        return
    button_error()
    return list_var, name_original


def trans_result(foo_var_2, foo_var_3):
    button_bloquear.config(state="disabled")
    original_final = []
    translated_final = []
    combined_final = []
    if foo_var_2[0] == 0:
        original_final = extract_w(foo_var_3)
        original_final = cleansing_w(original_final, dict_spacy[foo_var_2[6]])
        original_final = lemmatization_w(original_final, dict_spacy[foo_var_2[6]])
        translated_final = translation_w(original_final, dict_trans[foo_var_2[6]], dict_trans[foo_var_2[7]])
    elif foo_var_2[0] == 1:
        original_final = extract_s(foo_var_3)
        translated_final = translation_s(original_final, dict_trans[foo_var_2[6]], dict_trans[foo_var_2[7]])
    else:
        original_final = extract_p(foo_var_3)
        translated_final = translation_p(original_final, dict_trans[foo_var_2[6]], dict_trans[foo_var_2[7]])
    for _ in range(len(translated_final)):
        if translated_final[_] == "Translation Error":
            del translated_final[_]
            del original_final[_]
        else:
            combined_final.append([original_final[_], translated_final[_]])
    if foo_var_2[1] == 0:
        xlsx_case(foo_var_2, combined_final)
    else:
        word_case(foo_var_2, combined_final)
    button_bloquear.config(state="normal", text="Desbloquear")
    button_iniciar.config(state="disabled")
    messagebox.showinfo("Proceso exitoso", "Se ha traducido correctamente el archivo.")
    return


def combined_fun():
    try:
        foo_var_4 = inicio_check()
        trans_result(foo_var_4[0], foo_var_4[1])
    except TypeError:
        return


# endregion

# region Widgets
root = Tk()
root.title("Página principal")
root.geometry("450x220")
source_idiomas = StringVar()
final_idiomas = StringVar()

label_archivo = Label(root, text="Dirección del archivo a traducir")
entry_archivo = Entry(root)
label_original = Label(root, text="Nombre del archivo a traducir")
entry_original = Entry(root)
label_destino = Label(root, text="Dirección del archivo traducido")
entry_destino = Entry(root)
label_name = Label(root, text="Nombre del archivo nuevo")
entry_name = Entry(root)

label_modo = Label(root, text="Modo")
label_palabra = Label(root, text="Palabras")
button_palabra = Button(root, text="Seleccionar")
label_oracion = Label(root, text="Oraciones")
button_oracion = Button(root, text="Seleccionar")
label_parrafo = Label(root, text="Párrafos")
button_parrafo = Button(root, text="Seleccionar")
button_list_mode.extend([button_palabra, button_oracion, button_parrafo])
for _ in range(len(button_list_mode)):
    button_list_mode[_].config(command=lambda b=button_list_mode[_]: select(b, button_list_mode))

label_tipo = Label(root, text="Destino")
label_excel = Label(root, text="Excel")
button_excel = Button(root, text="Seleccionar")
label_word = Label(root, text="Word")
button_word = Button(root, text="Seleccionar")
button_list_file.extend([button_excel, button_word])
for _ in range(len(button_list_file)):
    button_list_file[_].config(command=lambda b=button_list_file[_]: select(b, button_list_file))

label_source = Label(root, text="Idioma de origen")
combobox_source = ttk.Combobox(root, textvariable=source_idiomas, values=list(reverse_dict.keys()))
label_exit = Label(root, text="Idioma destino")
combobox_exit = ttk.Combobox(root, textvariable=final_idiomas, values=list(reverse_dict.keys()))

button_instrucciones = Button(root, text="Instrucciones", command=instr)
button_iniciar = Button(root, text="Iniciar", state="disabled", command=combined_fun)
button_bloquear = Button(root, text="Desbloquear", command=desbloquear)
# endregion

# region Grid
label_archivo.grid(row=0, column=0, columnspan=2)
entry_archivo.grid(row=0, column=2, columnspan=4)
label_original.grid(row=1, column=0, columnspan=2)
entry_original.grid(row=1, column=2, columnspan=4)
label_destino.grid(row=2, column=0, columnspan=2)
entry_destino.grid(row=2, column=2, columnspan=4)
label_name.grid(row=3, column=0, columnspan=2)
entry_name.grid(row=3, column=2, columnspan=4)

label_modo.grid(row=4, column=0, columnspan=2)
label_palabra.grid(row=5, column=0)
button_palabra.grid(row=5, column=1)
label_oracion.grid(row=6, column=0)
button_oracion.grid(row=6, column=1)
label_parrafo.grid(row=7, column=0)
button_parrafo.grid(row=7, column=1)

label_tipo.grid(row=4, column=2, columnspan=2)
label_excel.grid(row=5, column=2)
button_excel.grid(row=5, column=3)
label_word.grid(row=6, column=2)
button_word.grid(row=6, column=3)

label_source.grid(row=4, column=4)
combobox_source.grid(row=5, column=4)
label_exit.grid(row=6, column=4)
combobox_exit.grid(row=7, column=4)

button_instrucciones.grid(row=8, column=0, rowspan=2)
button_iniciar.grid(row=8, column=4)
button_bloquear.grid(row=8, column=3)

root.mainloop()
# endregion
