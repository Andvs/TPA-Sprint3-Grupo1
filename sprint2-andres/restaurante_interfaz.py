from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QLineEdit, QMessageBox
from PyQt6.QtCore import pyqtSignal


class RestauranteInterfaz(QWidget):

    mi_signal = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.nombre = None
        self.seccion = 'Restaurante'
        self.tipo = None

        self.setWindowTitle("Restaurante")
        
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        label_nombre = QLabel("Nombre de la Persona:")
        self.input_nombre = QLineEdit()
        layout.addWidget(label_nombre)
        layout.addWidget(self.input_nombre)
        
        label_plan = QLabel("Seleccione un Plan de Comida:")
        self.combo_plan = QComboBox()
        self.combo_plan.addItem("Inicial")
        self.combo_plan.addItem("Intermedio")
        self.combo_plan.addItem("Completo")
        self.combo_plan.addItem("Avanzado")
        self.combo_plan.addItem("Premium")
        layout.addWidget(label_plan)
        layout.addWidget(self.combo_plan)
        
        button_reservar = QPushButton("Reservar Plan")
        button_reservar.clicked.connect(self.reservar_plan)
        layout.addWidget(button_reservar)

        button_actualizar = QPushButton("Actualizar Reserva")
        button_actualizar.clicked.connect(self.actualizar_reserva)
        layout.addWidget(button_actualizar)

        button_eliminar = QPushButton("Eliminar Reserva")
        button_eliminar.clicked.connect(self.eliminar_reserva)
        layout.addWidget(button_eliminar)
        
        self.setLayout(layout)
    
    
    def reservar_plan(self):
        self.nombre = self.input_nombre.text()
        self.tipo = self.combo_plan.currentText()

        for i in self.nombre:
            if i in '0123456789':
                return QMessageBox.warning(self, "Error", "Por favor, ingrese un dato valido.") and self.input_nombre.clear()
        
        for i in self.nombre:
            if i in '!"#$%&/()=?¡¿@,;.:-{[]^}<>¨´*+~':
                return QMessageBox.warning(self, "Error", "Por favor, ingrese un dato valido.") and self.input_nombre.clear()

            
        
        if self.nombre and self.tipo:
            mensaje = f"Plan de Comida Reservado:\n\nNombre: {self.nombre}\nPlan: {self.tipo}"
            QMessageBox.information(self, "Reserva Exitosa", mensaje)
            
            self.input_nombre.clear()

            #agregar los datos de la reserva al archivo csv
            try:
                texto_csv = open('sprint2-andres\\archivo_reservas.csv', 'a')
                texto_csv.write(f"'{self.nombre}','Restaurante', '{self.tipo}'\n")
                texto_csv.close()
            except Exception as e:
                print(f'El archivo no se encuentra ... {e}')

            self.mi_signal.emit()

        else:
            QMessageBox.warning(self, "Error", "Por favor, complete el nombre y seleccione un plan de comida.")
    

    def actualizar_reserva(self):
        
        archivo = 'sprint2-andres\\archivo_reservas.csv'
        self.nombre = self.input_nombre.text()
        self.tipo = self.combo_plan.currentText()

        for i in self.nombre:
            if i in '0123456789':
                return QMessageBox.warning(self, "Error", "Por favor, ingrese un dato valido.") and self.input_nombre.clear()
        
        for i in self.nombre:
            if i in '!"#$%&/()=?¡¿@,;.:-{[]^}<>¨´*+~':
                return QMessageBox.warning(self, "Error", "Por favor, ingrese un dato valido.") and self.input_nombre.clear()


        if self.nombre and self.tipo:

            num_linea_reserva = self.encontrar_elemento_archivo(archivo, self.nombre, None)
            nueva_linea = f"'{self.nombre}', 'Reserva de habitacion', '{self.tipo}'"
            self.modificar_linea(archivo, num_linea_reserva, nueva_linea)

            self.mi_signal.emit()
            self.input_nombre.clear()
            QMessageBox.information(self, "Reserva Actualizada", "Reserva actualizada exitosamente.")
                    
        else:
            QMessageBox.warning(self, "Error", "Por favor, complete el nombre y seleccione un plan de comida.")


    def eliminar_reserva(self):
        
        archivo = 'sprint2-andres\\archivo_reservas.csv'

        nombre_reserva = self.input_nombre.text()
        tipo = self.combo_plan.currentText()

        linea_reserva = self.encontrar_elemento_archivo(archivo, nombre_reserva, tipo)
        
        if linea_reserva == None:
            QMessageBox.warning(self, "Error", "Esa persona no tiene una reserva con esas características.")
        else:
            self.eliminar_linea_archivo(archivo, linea_reserva)
            QMessageBox.information(self, "Reserva Eliminada", "Reserva eliminada exitosamente.")

        self.mi_signal.emit()

    def eliminar_linea_archivo(self, archivo, numero_linea):
        with open(archivo, 'r') as archivo_origen:
            lineas = archivo_origen.readlines()

        # Verifica que el número de línea sea válido
        if numero_linea < 1 or numero_linea > len(lineas):
            print(numero_linea)
            print("Número de línea inválido")
            return

        # Elimina la línea deseada de la lista de líneas
        del lineas[numero_linea - 1]

        with open(archivo, 'w') as archivo_destino:
            archivo_destino.writelines(lineas)
    
    def encontrar_elemento_archivo(self, archivo, elemento1, elemento2):

        with open(archivo, 'r') as archivo_origen:
            linea_actual = 0

            for linea in archivo_origen:
                linea_actual += 1

                if elemento1 in linea and elemento2 == None:
                    return linea_actual

                if elemento1 in linea and elemento2 in linea:
                    return linea_actual
        
        return None
    
    def modificar_linea(self, archivo, linea_index, nueva_linea):
        with open(archivo, 'r') as file:
            lineas = file.readlines()
        
        linea_index -= 1
        if linea_index < 0 or linea_index >= len(lineas):
            print("Índice de línea inválido", linea_index, len(lineas))
            return

        lineas[linea_index] = nueva_linea + '\n'

        with open(archivo, 'w') as file:
            file.writelines(lineas)

    
