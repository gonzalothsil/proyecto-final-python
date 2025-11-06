import tkinter as tk
from tkinter import ttk, simpledialog, filedialog
import json

class FormBuilderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Creador de Formularios (Tkinter)")
        self.root.geometry("750x700")
        self.fields = []  # Campos del formulario

        # Canvas con scroll
        self.canvas = tk.Canvas(root)
        self.scroll_y = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.form_frame = tk.Frame(self.canvas)
        self.form_frame.bind(
            "<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.form_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll_y.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scroll_y.pack(side="right", fill="y")

        # Botones superiores
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Campo de Texto", command=self.add_text_field).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="CheckBox", command=self.add_checkbox).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Género (Radio)", command=self.add_radiobutton).grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="ComboBox", command=self.add_combobox).grid(row=0, column=3, padx=5)
        ttk.Button(button_frame, text="Botón Enviar", command=self.add_submit_button_field).grid(row=0, column=4, padx=5)
        ttk.Button(button_frame, text="Botón Vaciar", command=self.add_clear_button_field).grid(row=0, column=5, padx=5)
        ttk.Button(root, text="Cargar Formulario JSON", command=self.load_form_json).pack(pady=5)
        ttk.Button(root, text="Guardar Formulario HTML y JSON", command=self.save_form_html_json).pack(pady=5)

        self.result_label = tk.Label(root, text="Formulario cargado aquí", justify="left")
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

    def register_field(self, field_type, widget_creator, label=""):
        self.fields.append({"tipo": field_type, "widget_creator": widget_creator, "label": label})
        self.redraw_form()

    def move_up(self, index):
        if index > 0:
            self.fields[index], self.fields[index-1] = self.fields[index-1], self.fields[index]
            self.redraw_form()

    def move_down(self, index):
        if index < len(self.fields) - 1:
            self.fields[index], self.fields[index+1] = self.fields[index+1], self.fields[index]
            self.redraw_form()

    # === CAMPOS ===
    def add_text_field(self, label=None):
        if label is None:
            label = simpledialog.askstring("Campo de texto", "Ingrese el nombre del campo:")
            if not label:
                return
        def create(parent):
            if label:
                tk.Label(parent, text=label).pack(anchor="w")
            entry = ttk.Entry(parent)
            entry.pack(fill="x")
            parent.entry = entry
        self.register_field("text", create, label)

    def add_checkbox(self, label=None):
        if label is None:
            label = simpledialog.askstring("Checkbox", "Ingrese el nombre del campo:")
            if not label:
                return
        def create(parent):
            if label:
                tk.Label(parent, text=label).pack(anchor="w")
            var = tk.BooleanVar()
            cb = ttk.Checkbutton(parent, variable=var)
            cb.pack(anchor="w")
            parent.var = var
        self.register_field("checkbox", create, label)

    def add_radiobutton(self, label=None, options=None):
        if label is None:
            label = simpledialog.askstring("Grupo de Radio", "Ingrese el nombre del grupo:")
            if not label:
                return
        if options is None:
            options_str = simpledialog.askstring("Opciones", "Ingrese las opciones separadas por coma (,):")
            options = [o.strip() for o in options_str.split(",")] if options_str else []
        def create(parent):
            if label:
                tk.Label(parent, text=label).pack(anchor="w")
            var = tk.StringVar()
            for option in options:
                ttk.Radiobutton(parent, text=option, variable=var, value=option).pack(anchor="w")
            parent.var = var
        self.register_field("radio", create, label)

    def add_combobox(self, label=None, options=None):
        if label is None:
            label = simpledialog.askstring("ComboBox", "Ingrese el nombre del campo:")
            if not label:
                return
        if options is None:
            options_str = simpledialog.askstring("Opciones", "Ingrese las opciones separadas por coma (,):")
            options = [o.strip() for o in options_str.split(",")] if options_str else []
        def create(parent):
            if label:
                tk.Label(parent, text=label).pack(anchor="w")
            combo = ttk.Combobox(parent)
            combo["values"] = options
            combo.pack(fill="x")
            parent.combo = combo
        self.register_field("combobox", create, label)

    def add_submit_button_field(self, label="Enviar"):
        def create(parent):
            btn = ttk.Button(parent, text=label, command=self.show_form_data)
            btn.pack(pady=5)
        self.register_field("button_submit", create, label)

    def add_clear_button_field(self, label="Vaciar"):
        def create(parent):
            btn = ttk.Button(parent, text=label, command=self.clear_all_entries)
            btn.pack(pady=5)
        self.register_field("button_clear", create, label)

    # === FUNCIONALIDAD ===
    def clear_all_entries(self):
        for field in self.fields:
            parent = field.get("container")
            if field["tipo"] == "text" and hasattr(parent, "entry"):
                parent.entry.delete(0, tk.END)
            elif field["tipo"] == "checkbox" and hasattr(parent, "var"):
                parent.var.set(False)
            elif field["tipo"] == "radio" and hasattr(parent, "var"):
                parent.var.set("")
            elif field["tipo"] == "combobox" and hasattr(parent, "combo"):
                parent.combo.set("")

    def show_form_data(self):
        result = ""
        for field in self.fields:
            parent = field.get("container")
            if field["tipo"] == "text":
                result += f"{field['label']}: {parent.entry.get()}\n"
            elif field["tipo"] == "checkbox":
                result += f"{field['label']}: {'Sí' if parent.var.get() else 'No'}\n"
            elif field["tipo"] == "radio":
                result += f"{field['label']}: {parent.var.get()}\n"
            elif field["tipo"] == "combobox":
                result += f"{field['label']}: {parent.combo.get()}\n"
            elif field["tipo"] in ["button_submit", "button_clear"]:
                result += f"[Botón: {field['label']}]\n"
        self.result_label.config(text=result)

    def save_form_html_json(self):
        filename = simpledialog.askstring("Guardar HTML y JSON", "Nombre del archivo (sin .html o .json):")
        if not filename:
            return
        html_filename = filename + ".html"
        json_filename = filename + ".json"

        html = "<form>\n"
        form_data = []
        for field in self.fields:
            parent = field.get("container")
            label = field["label"]
            item = {"tipo": field["tipo"], "label": label}

            if field["tipo"] == "radio":
                # Guardar opciones
                options = [child.cget("text") for child in parent.winfo_children() if isinstance(child, ttk.Radiobutton)]
                item["options"] = options
            elif field["tipo"] == "combobox":
                item["options"] = list(parent.combo["values"])

            form_data.append(item)

            # Generar HTML
            if field["tipo"] == "text":
                html += f'<label>{label}:</label><br><input type="text"><br><br>\n'
            elif field["tipo"] == "checkbox":
                html += f'<label><input type="checkbox"> {label}</label><br><br>\n'
            elif field["tipo"] == "radio":
                html += f'<label>{label}:</label><br>\n'
                for option in item.get("options", []):
                    html += f'<input type="radio" name="{label}" value="{option}"> {option}<br>\n'
            elif field["tipo"] == "combobox":
                html += f'<label>{label}:</label><br>\n<select>\n'
                for option in item.get("options", []):
                    html += f'<option value="{option}">{option}</option>\n'
                html += '</select><br><br>\n'
        html += "</form>"

        with open(html_filename, "w", encoding="utf-8") as html_file:
            html_file.write(html)
        with open(json_filename, "w", encoding="utf-8") as json_file:
            json.dump(form_data, json_file, ensure_ascii=False, indent=2)

        self.result_label.config(text=f"Formulario guardado en: {html_filename} y {json_filename}")

    def load_form_json(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if not file_path:
            return
        with open(file_path, "r", encoding="utf-8") as json_file:
            form_data = json.load(json_file)

        self.fields.clear()

        for field_data in form_data:
            tipo = field_data["tipo"]
            label = field_data["label"]
            options = field_data.get("options", [])
            if tipo == "text":
                self.add_text_field(label)
            elif tipo == "checkbox":
                self.add_checkbox(label)
            elif tipo == "radio":
                self.add_radiobutton(label, options)
            elif tipo == "combobox":
                self.add_combobox(label, options)
            elif tipo == "button_submit":
                self.add_submit_button_field(label)
            elif tipo == "button_clear":
                self.add_clear_button_field(label)

        self.redraw_form()
        self.result_label.config(text=f"Formulario cargado desde: {file_path}")


if __name__ == "__main__":
    root = tk.Tk()
    app = FormBuilderApp(root)
    root.mainloop()
