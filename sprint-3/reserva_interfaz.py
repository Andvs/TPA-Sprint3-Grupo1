from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QMessageBox
from PyQt6.QtCore import pyqtSignal

class ReservaInterfaz(QWidget):

    mi_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        
        self.nombre = None
        self.seccion = 'Reserva de habitación'
        self.tipo = None

        self.setWindowTitle("Reserva")
        self.setFixedSize(300, 200)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        label_nombre = QLabel("Nombre de la Persona:")
        self.input_nombre = QLineEdit()
        layout.addWidget(label_nombre)
        layout.addWidget(self.input_nombre)
        
        label_habitacion = QLabel("Seleccione una Habitación:")
        self.combo_habitacion = QComboBox()
        self.combo_habitacion.addItem("Ejecutiva Individual")
        self.combo_habitacion.addItem("Ejecutiva Doble")
        self.combo_habitacion.addItem("Familiar")
        self.combo_habitacion.addItem("PentHouse Volcanes")
        self.combo_habitacion.addItem("PentHouse Pacífico")
        layout.addWidget(label_habitacion)
        layout.addWidget(self.combo_habitacion)
        
        button_reservar = QPushButton("Realizar Reserva")
        button_reservar.clicked.connect(self.agregar_reserva_habitacion)
        layout.addWidget(button_reservar)

        button_actualizar = QPushButton("Actualizar Reserva")
        button_actualizar.clicked.connect(self.actualizar_reserva)
        layout.addWidget(button_actualizar)

        button_eliminar = QPushButton("Eliminar Reserva")
        button_eliminar.clicked.connect(self.eliminar_reserva)
        layout.addWidget(button_eliminar)
        
        self.setLayout(layout)
    
    def agregar_reserva_habitacion(self):
        self.nombre = self.input_nombre.text()
        self.tipo = self.combo_habitacion.currentText()

        for i in self.nombre:
            if i in '0123456789':
                return QMessageBox.warning(self, "Error", "Por favor, ingrese un dato valido.") and self.input_nombre.clear()
        
        for i in self.nombre:
            if i in ''''!"#$%&/()=?¡¿@,;.:-{[]^}<>¨´*+~´''':
                return QMessageBox.warning(self, "Error", "Por favor, ingrese un dato valido.") and self.input_nombre.clear()
        
        if self.nombre and self.tipo:
            datos_para_guardar = f"'{self.nombre}', '{self.seccion}', '{self.tipo}'"
            verificar_nombre_seccion = f"'{self.nombre}', '{self.seccion}'"
            with open('sprint-3\\archivo_reservas.csv', 'r') as archivo_origen:
                    for linea in archivo_origen:
                        if datos_para_guardar in linea:
                            return QMessageBox.warning(self, "Error", "Estos datos ya existen.") and self.input_nombre.clear()
                        elif verificar_nombre_seccion in linea:
                            return QMessageBox.warning(self, "Error", "Esta persona ya tiene un reserva en esta sección. Utilice actualizar para cambiar la opción de reserva") and self.input_nombre.clear()

                        
        
        if self.nombre and self.tipo:
            
            try:
                precio = None
                if self.tipo == 'Ejecutiva Individual' :
                    precio = '$50.000'
                elif self.tipo == 'Ejecutiva Doble':
                    precio = '$80.000'
                elif self.tipo == 'Familiar':
                    precio = '$150.000'
                else:
                    precio = '$1.080.000'


                texto_csv = open('sprint-3\\archivo_reservas.csv', 'a')
                texto_csv.write(f"'{self.nombre}', '{self.seccion}', '{self.tipo}', {precio}\n")
                texto_csv.close()

                QMessageBox.information(self, "Reserva Exitosa", "Se ha realizado la reserva")
                
                self.mi_signal.emit()
                self.input_nombre.clear()
                self.close()

            except Exception as e:
                print(f'El archivo no se encuentra ... {e}')

            

        else:
            QMessageBox.warning(self, "Error", "Por favor, complete el nombre y seleccione una habitación.") 

    def actualizar_reserva(self):
        
        archivo = 'sprint-3\\archivo_reservas.csv'
        self.nombre = self.input_nombre.text()
        self.tipo = self.combo_habitacion.currentText()

        for i in self.nombre:
            if i in '0123456789':
                return QMessageBox.warning(self, "Error", "Por favor, ingrese un dato valido.") and self.input_nombre.clear()
        
        for i in self.nombre:
            if i in '!"#$%&/()=?¡¿@,;.:-{[]^}<>¨´*+~':
                return QMessageBox.warning(self, "Error", "Por favor, ingrese un dato valido.") and self.input_nombre.clear()


        if self.nombre and self.tipo:

            num_linea_reserva = self.encontrar_elemento_archivo(archivo, self.nombre, self.seccion)
            

            if num_linea_reserva == None:
                QMessageBox.warning(self, "Error", "Esa persona no tiene una reserva con esas características.")
    
            else:
                nueva_linea = f"'{self.nombre}', '{self.seccion}', '{self.tipo}'"
                self.modificar_linea(archivo, num_linea_reserva, nueva_linea)

                QMessageBox.information(self, "Reserva actulizada", "Reserva actualizada exitosamente.")
                self.mi_signal.emit()
                self.input_nombre.clear()
                self.close()

        else:
            QMessageBox.warning(self, "Error", "Por favor, complete el nombre y seleccione una habitación.")
        
    
    def eliminar_reserva(self):
        
        archivo = 'sprint-3\\archivo_reservas.csv'
        self.nombre = self.input_nombre.text()
        self.tipo = self.combo_habitacion.currentText()

        for i in self.nombre:
            if i in '0123456789':
                return QMessageBox.warning(self, "Error", "Por favor, ingrese un dato valido.") and self.input_nombre.clear()
        
        for i in self.nombre:
            if i in '!"#$%&/()=?¡¿@,;.:-{[]^}<>¨´*+~':
                return QMessageBox.warning(self, "Error", "Por favor, ingrese un dato valido.") and self.input_nombre.clear()

        if self.nombre and self.tipo:

            linea_reserva = self.encontrar_elemento_archivo(archivo, self.nombre, self.seccion, self.tipo)

            if linea_reserva == None:
                QMessageBox.warning(self, "Error", "Esa persona no tiene una reserva con esas características.")
    
            else:
                self.eliminar_linea_archivo(archivo, linea_reserva)
                QMessageBox.information(self, "Reserva Eliminada", "Reserva eliminada exitosamente.")
                self.mi_signal.emit()
                self.input_nombre.clear()
                self.close()
                
        else:
            return QMessageBox.warning(self, "Error", "Ingrese un nombre.")
        
        
        

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
    
    def encontrar_elemento_archivo(self, archivo, nombre, seccion, tipo = None):

        if tipo == None:
            linea_datos = f"'{nombre}', '{seccion}'"
            
        else:
            linea_datos = f"'{nombre}', '{seccion}', '{self.tipo}'"
            
            
        with open(archivo, 'r') as archivo_origen:
            linea_actual = 0

            for linea in archivo_origen:
                
                linea_actual += 1

                if linea_datos in linea:
                    
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
