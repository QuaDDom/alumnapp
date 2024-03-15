import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QLineEdit, QDialog, QMessageBox, QColorDialog, QHeaderView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mi Aplicación")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.create_button = QPushButton("Crear")
        self.create_button.clicked.connect(self.create_data_window)

        self.modify_button = QPushButton("Modificar")
        self.modify_button.clicked.connect(self.modify_data)

        self.delete_button = QPushButton("Eliminar")
        self.delete_button.clicked.connect(self.delete_data)

        self.change_color_button = QPushButton("Cambiar Colores")
        self.change_color_button.clicked.connect(self.change_colors)

        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.create_button)
        self.button_layout.addWidget(self.modify_button)
        self.button_layout.addWidget(self.delete_button)
        self.button_layout.addWidget(self.change_color_button)

        self.layout.addLayout(self.button_layout)

        self.data_table = QTableWidget()
        self.data_table.setColumnCount(4)
        self.data_table.setHorizontalHeaderLabels(["Nombre", "Apellido", "Email", "Curso"])
        self.data_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.data_table)

    def create_data_window(self):
        dialog = DataDialog(self)
        if dialog.exec_():
            data = dialog.get_data()
            row_position = self.data_table.rowCount()
            self.data_table.insertRow(row_position)
            for column, value in enumerate(data.values()):
                self.data_table.setItem(row_position, column, QTableWidgetItem(value))

    def modify_data(self):
        selected_row = self.data_table.currentRow()
        if selected_row != -1:
            dialog = DataDialog(self, modify=True)
            if dialog.exec_():
                data = dialog.get_data()
                for column, value in enumerate(data.values()):
                    self.data_table.setItem(selected_row, column, QTableWidgetItem(value))
        else:
            QMessageBox.information(self, "Información", "Por favor, seleccione un dato para modificar")

    def delete_data(self):
        self.data_table.clearContents()

    def change_colors(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.setStyleSheet(f"background-color: {color.name()};")


class DataDialog(QDialog):
    def __init__(self, parent, modify=False):
        super().__init__(parent)
        self.setWindowTitle("Cargar Datos")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.data = {}

        self.nombre_label = QLabel("Nombre:")
        self.nombre_input = QLineEdit()
        self.layout.addWidget(self.nombre_label)
        self.layout.addWidget(self.nombre_input)

        self.apellido_label = QLabel("Apellido:")
        self.apellido_input = QLineEdit()
        self.layout.addWidget(self.apellido_label)
        self.layout.addWidget(self.apellido_input)

        self.email_label = QLabel("Email:")
        self.email_input = QLineEdit()
        self.layout.addWidget(self.email_label)
        self.layout.addWidget(self.email_input)

        self.curso_label = QLabel("Curso:")
        self.curso_input = QLineEdit()
        self.layout.addWidget(self.curso_label)
        self.layout.addWidget(self.curso_input)

        self.buttons_layout = QHBoxLayout()
        self.accept_button = QPushButton("Aceptar")
        self.accept_button.clicked.connect(self.accept)
        self.buttons_layout.addWidget(self.accept_button)

        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.clicked.connect(self.reject)
        self.buttons_layout.addWidget(self.cancel_button)

        self.layout.addLayout(self.buttons_layout)

        if modify:
            self.setWindowTitle("Modificar Datos")
            self.fill_data()

    def fill_data(self):
        parent = self.parent()
        selected_row = parent.data_table.currentRow()
        if selected_row != -1:
            for column in range(parent.data_table.columnCount()):
                item = parent.data_table.item(selected_row, column)
                header = parent.data_table.horizontalHeaderItem(column).text()
                self.data[header.lower()] = item.text()

        self.nombre_input.setText(self.data.get('nombre', ''))
        self.apellido_input.setText(self.data.get('apellido', ''))
        self.email_input.setText(self.data.get('email', ''))
        self.curso_input.setText(self.data.get('curso', ''))

    def get_data(self):
        self.data['nombre'] = self.nombre_input.text()
        self.data['apellido'] = self.apellido_input.text()
        self.data['email'] = self.email_input.text()
        self.data['curso'] = self.curso_input.text()
        return self.data


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
