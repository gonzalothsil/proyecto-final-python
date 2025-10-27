import tkinter as tk
from tkinter import ttk, simpledialog
import json

class FormBuilderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Creador de Formularios (Tkinter)")
        self.root.geometry("700x650")

        self.fields = []

        self.canvas = tk.Canvas(root)
        self.scroll_y = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.form_frame = tk.Frame(self.canvas)

        self.form_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.form_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll_y.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scroll_y.pack(side="right", fill="y")

        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Añadir Campo de Texto", command=self.add_text_field).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Añadir CheckBox", command=self.add_checkbox).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Añadir Género (Radio)", command=self.add_radiobutton).grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="Añadir ComboBox", command=self.add_combobox).grid(row=0, column=3, padx=5)

        ttk.Button(root, text="Obtener Datos del Formulario", command=self.show_form_data).pack(pady=5)
        ttk.Button(root, text="Guardar Formulario HTML", command=self.save_form_html).pack(pady=5)

        self.result_label = tk.Label(root, text="Datos del formulario aparecerán aquí", justify="left")
        self.result_label.pack(pady=10)

    def redraw_form(self):
        for widget in self.form_frame.winfo_children():
            widget.destroy()

        for index, field in enumerate(self.fields):
            frame = tk.Frame(self.form_frame, pady=3)
            frame.pack(fill="x")

            tk.Button(frame, text="↑", width=2, command=lambda i=index: self.move_up(i)).pack(side="left")
            tk.Button(frame, text="↓", width=2, command=lambda i=index: self.move_down(i)).pack(side="left")

            container = tk.Frame(frame)
            container.pack(side="left", fill="x", expand=True)

            field['widget_creator'](container)
            field['container'] = container

    def register_field(self, field_type, widget_creator):
        self.fields.append({"tipo": field_type, "widget_creator": widget_creator})
        self.redraw_form()

    def move_up(self, index):
        if index > 0:
            self.fields[index], self.fields[index-1] = self.fields[index-1], self.fields[index]
            self.redraw_form()

    def move_down(self, index):
        if index < len(self.fields) - 1:
            self.fields[index], self.fields[index+1] = self.fields[index+1], self.fields[index]
            self.redraw_form()

    def add_text_field(self):
        text_label = simpledialog.askstring("Etiqueta", "Nombre del campo:")
        if not text_label: text_label = "Campo de Texto"

        def create(parent):
            tk.Label(parent, text=text_label).pack(anchor="w")
            entry = ttk.Entry(parent)
            entry.pack(fill="x")
            parent.entry = entry
            parent.label = text_label

        self.register_field("text", create)

    def add_checkbox(self):
        check_text = simpledialog.askstring("Texto del CheckBox", "Texto que mostrará:")
        if not check_text: check_text = "Acepto los términos"

        def create(parent):
            var = tk.BooleanVar()
            cb = ttk.Checkbutton(parent, text=check_text, variable=var)
            cb.pack(anchor="w")
            parent.var = var
            parent.text = check_text

        self.register_field("checkbox", create)

    def add_radiobutton(self):
        label_text = simpledialog.askstring("Etiqueta", "Texto del grupo (ej: Género):")
        if not label_text: label_text = "Género"

        def create(parent):
            tk.Label(parent, text=label_text).pack(anchor="w")
            var = tk.StringVar()
            ttk.Radiobutton(parent, text="Masculino", variable=var, value="Masculino").pack(anchor="w")
            ttk.Radiobutton(parent, text="Femenino", variable=var, value="Femenino").pack(anchor="w")
            parent.var = var
            parent.label = label_text

        self.register_field("radio", create)

    def add_combobox(self):
        label_text = simpledialog.askstring("Etiqueta", "Texto del ComboBox:")
        if not label_text: label_text = "Seleccione una opción"

        options = simpledialog.askstring("Opciones", "Ingrese opciones separadas por coma (,):")
        if options:
            option_list = [o.strip() for o in options.split(",")]
        else:
            option_list = ["Opción 1", "Opción 2"]

        def create(parent):
            tk.Label(parent, text=label_text).pack(anchor="w")
            combo = ttk.Combobox(parent, values=option_list)
            combo.pack(fill="x")
            parent.combo = combo
            parent.label = label_text
            parent.options = option_list

        self.register_field("combobox", create)

    def show_form_data(self):
        result = ""

        for field in self.fields:
            parent = field.get("container")

            if field["tipo"] == "text":
                result += f"{parent.label}: {parent.entry.get()}\n"
            elif field["tipo"] == "checkbox":
                result += f"{parent.text}: {'Sí' if parent.var.get() else 'No'}\n"
            elif field["tipo"] == "radio":
                result += f"{parent.label}: {parent.var.get()}\n"
            elif field["tipo"] == "combobox":
                result += f"{parent.label}: {parent.combo.get()}\n"

        self.result_label.config(text=result)

    def save_form_html(self):
        filename = simpledialog.askstring("Guardar HTML", "Nombre del archivo (sin .html):")
        if not filename: return
        filename += ".html"

        html = "<form>\n"
        for field in self.fields:
            parent = field.get("container")
            if field["tipo"] == "text":
                html += f'<label>{parent.label}:</label><br><input type="text"><br><br>\n'
            elif field["tipo"] == "checkbox":
                html += f'<label><input type="checkbox"> {parent.text}</label><br><br>\n'
            elif field["tipo"] == "radio":
                html += f"<label>{parent.label}:</label><br>\n"
                html += '<input type="radio" name="radio" value="Masculino"> Masculino<br>\n'
                html += '<input type="radio" name="radio" value="Femenino"> Femenino<br><br>\n'
            elif field["tipo"] == "combobox":
                html += f"<label>{parent.label}:</label><br>\n<select>\n"
                for opt in parent.options:
                    html += f"  <option>{opt}</option>\n"
                html += "</select><br><br>\n"
        html += "</form>"

        with open(filename, "w", encoding="utf-8") as file:
            file.write(html)

        self.result_label.config(text=f"✅ Formulario guardado como: {filename}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FormBuilderApp(root)
    root.mainloop()

