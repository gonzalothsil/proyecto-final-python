import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QCheckBox, QComboBox, QRadioButton, QFormLayout, QGroupBox, QScrollArea
from PyQt6.QtCore import Qt

class FormBuilderApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Creador de Formularios")
        self.setGeometry(100, 100, 800, 600)
        
        # Layout principal
        self.main_layout = QVBoxLayout()

        # Layout para el formulario dinámico
        self.form_layout = QFormLayout()
        self.form_groupbox = QGroupBox("Formulario")
        self.form_groupbox.setLayout(self.form_layout)
        
        # Scroll area para poder ver el formulario largo
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.form_groupbox)
        self.scroll_area.setWidgetResizable(True)
        self.main_layout.addWidget(self.scroll_area)

        # Botones para agregar widgets al formulario
        self.add_field_layout = QHBoxLayout()
        self.add_text_button = QPushButton("Añadir Campo de Texto")
        self.add_checkbox_button = QPushButton("Añadir Casilla de Verificación")
        self.add_radiobutton_button = QPushButton("Añadir Opción de Género")
        self.add_combobox_button = QPushButton("Añadir Combo Box")

        self.add_field_layout.addWidget(self.add_text_button)
        self.add_field_layout.addWidget(self.add_checkbox_button)
        self.add_field_layout.addWidget(self.add_radiobutton_button)
        self.add_field_layout.addWidget(self.add_combobox_button)
        
        # Conectar los botones con sus funciones
        self.add_text_button.clicked.connect(self.add_text_field)
        self.add_checkbox_button.clicked.connect(self.add_checkbox)
        self.add_radiobutton_button.clicked.connect(self.add_radiobutton)
        self.add_combobox_button.clicked.connect(self.add_combobox)

        # Agregar los botones para añadir widgets
        self.main_layout.addLayout(self.add_field_layout)

        # Botón para obtener los datos del formulario
        self.submit_button = QPushButton("Obtener Datos del Formulario")
        self.submit_button.clicked.connect(self.show_form_data)
        self.main_layout.addWidget(self.submit_button)

        # Etiqueta para mostrar los datos del formulario
        self.result_label = QLabel("Datos del formulario aparecerán aquí")
        self.main_layout.addWidget(self.result_label)

        self.setLayout(self.main_layout)

    def add_text_field(self):
        """Añadir un campo de texto (QLineEdit) al formulario."""
        text_field = QLineEdit(self)
        self.form_layout.addRow("Campo de Texto", text_field)

    def add_checkbox(self):
        """Añadir una casilla de verificación (QCheckBox) al formulario."""
        checkbox = QCheckBox("Acepto los términos y condiciones", self)
        self.form_layout.addRow("", checkbox)

    def add_radiobutton(self):
        """Añadir opciones de género con radio buttons (QRadioButton)."""
        radio_male = QRadioButton("Masculino", self)
        radio_female = QRadioButton("Femenino", self)
        self.form_layout.addRow("Género", radio_male)
        self.form_layout.addRow("", radio_female)

    def add_combobox(self):
        """Añadir un combo box (QComboBox) al formulario."""
        combobox = QComboBox(self)
        combobox.addItems(["Opción 1", "Opción 2", "Opción 3"])
        self.form_layout.addRow("Selecciona una opción", combobox)

    def show_form_data(self):
        """Obtener y mostrar los datos ingresados en el formulario."""
        form_data = ""
        
        # Recolectar los datos de los widgets en el formulario
        for i in range(self.form_layout.rowCount()):
            widget = self.form_layout.itemAt(i, QFormLayout.FieldRole).widget()
            
            if isinstance(widget, QLineEdit):
                form_data += f"{self.form_layout.labelForField(widget).text()}: {widget.text()}\n"
            elif isinstance(widget, QCheckBox):
                form_data += f"{widget.text()}: {'Sí' if widget.isChecked() else 'No'}\n"
            elif isinstance(widget, QRadioButton):
                if widget.isChecked():
                    form_data += f"{self.form_layout.labelForField(widget).text()}: {widget.text()}\n"
            elif isinstance(widget, QComboBox):
                form_data += f"{self.form_layout.labelForField(widget).text()}: {widget.currentText()}\n"
        
        # Mostrar los datos
        self.result_label.setText(form_data)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form_app = FormBuilderApp()
    form_app.show()
    sys.exit(app.exec())
