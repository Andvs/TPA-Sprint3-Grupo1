from PyQt6.QtWidgets import QWidget, QLabel, QDateEdit, QLineEdit, QComboBox, QPushButton, QMessageBox, QGridLayout, QCalendarWidget
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtCore import QDate

class ReservaInterfaz(QWidget):

    mi_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        
        self.nombre = None
        self.reserva_habitacion = None
        self.reserva_excursion = None
        self.reserva_restaurante = None
        

        self.setWindowTitle("Reserva")
        self.setFixedSize(300, 400)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QGridLayout()
        
        #nombre
        label_nombre = QLabel("Nombre de la Persona:")
        self.input_nombre = QLineEdit()
        layout.addWidget(label_nombre, 0,0, 1,2)
        layout.addWidget(self.input_nombre, 1,0, 1,2)

        #fecha inicio y final
        inicio_fecha_label = QLabel('Fecha de inicio:')
        layout.addWidget(inicio_fecha_label, 2,0, 1,2)

        self.inicio_fecha = QDateEdit()
        self.inicio_fecha.setCalendarPopup(True)
        self.inicio_fecha.setDate(QDate.currentDate())
        self.inicio_fecha.dateChanged.connect(self.diferencia_dias)
        layout.addWidget(self.inicio_fecha, 3,0, 1,2)

        final_fecha_label = QLabel('Fecha de finalización:')
        layout.addWidget(final_fecha_label, 4,0, 1,2)

        self.final_fecha = QDateEdit()
        self.final_fecha.setCalendarPopup(True)
        self.final_fecha.setDate(QDate.currentDate())
        layout.addWidget(self.final_fecha, 5,0, 1,2)

        #reserva habitación

        label_habitacion = QLabel("Seleccione una Habitación:")
        self.combo_habitacion = QComboBox()
        self.combo_habitacion.addItem("Ejecutiva Individual")
        self.combo_habitacion.addItem("Ejecutiva Doble")
        self.combo_habitacion.addItem("Familiar")
        self.combo_habitacion.addItem("PentHouse Volcanes")
        self.combo_habitacion.addItem("PentHouse Pacífico")
        layout.addWidget(label_habitacion, 6,0, 1,2)
        layout.addWidget(self.combo_habitacion, 7,0, 1,2)
        

        #reserva turismo
        
        label_excursion = QLabel("Seleccione una Excursión:")
        self.combo_excursion = QComboBox()
        self.combo_excursion.addItem("Ninguno")
        self.combo_excursion.addItem("Excursión Light")
        self.combo_excursion.addItem("Excursión Plus")
        self.combo_excursion.addItem("Excursión Heavy")
        
        layout.addWidget(label_excursion, 8,0, 1,2)
        layout.addWidget(self.combo_excursion, 9,0, 1,2)
        
        
        #reserva restaurante
        
        label_plan = QLabel("Seleccione un Plan de Comida:")
        self.combo_plan = QComboBox()
        self.combo_plan.addItem("Ninguno")
        self.combo_plan.addItem("Inicial")
        self.combo_plan.addItem("Intermedio")
        self.combo_plan.addItem("Completo")
        self.combo_plan.addItem("Avanzado")
        self.combo_plan.addItem("Premium")
        layout.addWidget(label_plan, 10,0, 1,2)
        layout.addWidget(self.combo_plan, 11,0, 1,2)

        button_cancelar= QPushButton("Cancelar")
        button_cancelar.clicked.connect(self.close)
        layout.addWidget(button_cancelar, 13,0, 2,1)

        button_reservar = QPushButton("Realizar Reserva")
        button_reservar.clicked.connect(self.agregar_reserva)
        layout.addWidget(button_reservar, 13,1, 2,1)


        self.setLayout(layout)
    
    def agregar_reserva(self):
        self.nombre = self.input_nombre.text()
        self.reserva_habitacion = self.combo_habitacion.currentText()
        self.reserva_excursion = self.combo_excursion.currentText()
        self.reserva_restaurante = self.combo_plan.currentText()

    

        for i in self.nombre:
            if i in '0123456789':
                return QMessageBox.warning(self, "Error", "Por favor, ingrese un dato valido.") and self.input_nombre.clear()
        
        for i in self.nombre:
            if i in ''''!"#$%&/()=?¡¿@,;.:-{[]^}<>¨´*+~´''':
                return QMessageBox.warning(self, "Error", "Por favor, ingrese un dato valido.") and self.input_nombre.clear()
        
        if self.nombre:
            datos_para_guardar = f"'{self.nombre}', '{self.reserva_habitacion}-{self.reserva_excursion}-{self.reserva_restaurante}'"
            
            with open('sprint-3\\archivo_reservas.csv', 'r') as archivo_origen:
                    for linea in archivo_origen:
                        if datos_para_guardar in linea:
                            return QMessageBox.warning(self, "Error", "Esta persona ya tiene una reserva.") and self.input_nombre.clear()
                        
        
        if self.nombre and self.final_fecha.date() > self.inicio_fecha.date():
            
            try:

                precio_reserva_habitacion = 0

                if self.reserva_habitacion == 'Ejecutiva Individual' :
                    precio_reserva_habitacion = 50000
                elif self.reserva_habitacion == 'Ejecutiva Doble':
                    precio_reserva_habitacion = 80000
                elif self.reserva_habitacion == 'Familiar':
                    precio_reserva_habitacion = 150000
                elif 'PentHouse' in self.reserva_habitacion:
                    precio_reserva_habitacion = 1080000

                precio_reserva_excursion = 0
                if self.reserva_excursion == 'Excursión Light' :
                    precio_reserva_excursion = 5000
                elif self.reserva_excursion == 'Excursión Plus':
                    precio_reserva_excursion = 25000
                elif self.reserva_excursion == 'Excursión Heavy':
                    precio_reserva_excursion = 50000
                

                precio_reserva_restaurante = 0
                if self.reserva_restaurante == 'Inicial' :
                    precio_reserva_restaurante = 10000
                elif self.reserva_restaurante == 'Intermedio':
                    precio_reserva_restaurante = 25000
                elif self.reserva_restaurante == 'Completo':
                    precio_reserva_restaurante = 45000
                elif self.reserva_restaurante == 'Avanzado':
                    precio_reserva_restaurante = 60000
                elif self.reserva_restaurante == 'Premium':
                    precio_reserva_restaurante = 100000
                    
                
                costo_total = precio_reserva_habitacion * self.diferencia_dias() + precio_reserva_restaurante + precio_reserva_excursion
                costo_total_str = "${:,.0f}".format(costo_total).replace(",", ".")

                texto_csv = open('sprint-3\\archivo_reservas.csv', 'a')
                texto_csv.write(f"'{self.nombre}', 'Habitación: {self.reserva_habitacion} | Excursión: {self.reserva_excursion} | Restaurante: {self.reserva_restaurante}', '{self.diferencia_dias()}','{costo_total_str}'\n")
                texto_csv.close()

                QMessageBox.information(self, "Reserva Exitosa", "Se ha realizado la reserva")
                
                self.mi_signal.emit()
                self.input_nombre.clear()
                self.close()

            except Exception as e:
                print(self.final_fecha.date())
                print(f'El archivo no se encuentra ... {e}')

        else:
            QMessageBox.warning(self, "Error", "Verifique que la fecha de inicio y final sean correctas") 

    def diferencia_dias(self):
        inicio = self.inicio_fecha.date()
        final = self.final_fecha.date()

        if inicio.isValid() and final.isValid():
            diferencia = inicio.daysTo(final)
            return diferencia
        
