from PyQt6.QtWidgets import QWidget, QLabel, QDateEdit, QLineEdit, QComboBox, QPushButton, QMessageBox, QGridLayout, QCalendarWidget
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtCore import QDate

class ActualizarReservaInterfaz(QWidget):

    mi_signal = pyqtSignal()

    def __init__(self, posicion_tabla):
        super().__init__()
        
        self.nombre = None
        self.reserva_habitacion = None
        self.reserva_excursion = None
        self.reserva_restaurante = None
        self.linea_tabla = posicion_tabla

        self.setWindowTitle("Actualizar reserva")
        self.setFixedSize(300, 400)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QGridLayout()
        
        #nombre de la persona
        label_nombre = QLabel("Nombre de la Persona:")

        #Se busca el nombre de la persona de la reserva para 
        #actualizar.
        with open('sprint-3\\archivo_reservas.csv', 'r') as file:
            lineas = file.readlines()
            datos = lineas[self.linea_tabla].split(',')
            nombre_reserva = datos[0].replace("'", "")

        #se agrega el nombre de la persona y se coloca en el QLineEdit sin posibilidad
        # de ser cambiado 
        self.input_nombre = QLineEdit()
        self.input_nombre.setReadOnly(True)
        self.input_nombre.setText(nombre_reserva)

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
        self.final_fecha.setDate(QDate.currentDate().addDays(1))
        layout.addWidget(self.final_fecha, 5,0, 1,2)

        #reserva habitación

        label_habitacion = QLabel("Seleccione una Habitación:")
        self.combo_habitacion = QComboBox()
        self.combo_habitacion.addItem("Ejecutiva Individual ($50.000)")
        self.combo_habitacion.addItem("Ejecutiva Doble ($80.000)")
        self.combo_habitacion.addItem("Familiar ($150.000)")
        self.combo_habitacion.addItem("PentHouse Volcanes ($1.080.000)")
        self.combo_habitacion.addItem("PentHouse Pacífico ($1.080.000)")
        layout.addWidget(label_habitacion, 6,0, 1,2)
        layout.addWidget(self.combo_habitacion, 7,0, 1,2)
        

        #reserva turismo
        
        label_excursion = QLabel("Seleccione una Excursión:")
        self.combo_excursion = QComboBox()
        self.combo_excursion.addItem("Ninguno")
        self.combo_excursion.addItem("Excursión Light ($5.000)")
        self.combo_excursion.addItem("Excursión Plus ($25.000)")
        self.combo_excursion.addItem("Excursión Heavy ($50.000)")
        
        layout.addWidget(label_excursion, 8,0, 1,2)
        layout.addWidget(self.combo_excursion, 9,0, 1,2)
        
        
        #reserva restaurante
        
        label_plan = QLabel("Seleccione un Plan de Comida:")
        self.combo_plan = QComboBox()
        self.combo_plan.addItem("Ninguno")
        self.combo_plan.addItem("Inicial ($10.000)")
        self.combo_plan.addItem("Intermedio ($25.000)")
        self.combo_plan.addItem("Completo ($45.000)")
        self.combo_plan.addItem("Avanzado ($60.000)")
        self.combo_plan.addItem("Premium ($100.000)")
        layout.addWidget(label_plan, 10,0, 1,2)
        layout.addWidget(self.combo_plan, 11,0, 1,2)

        button_cancelar= QPushButton("Cancelar")
        button_cancelar.clicked.connect(self.close)
        layout.addWidget(button_cancelar, 13,0, 2,1)

        button_reservar = QPushButton("Actualizar Reserva")
        button_reservar.clicked.connect(self.agregar_nueva_reserva)
        layout.addWidget(button_reservar, 13,1, 2,1)


        self.setLayout(layout)


    #Añade la reserva con los datos nombre, habitacion, excursion y plan de restaurante seleccionados.
    #Se asigna el correspondiente valor a cada opción seleccionada y se suma para dar el total.
    #Estos datos se guardan en el archivo csv.
    
    def agregar_nueva_reserva(self):
            
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
        
                   
        
        if self.nombre and self.final_fecha.date() > self.inicio_fecha.date():
            
            try:
                 
                precio_reserva_habitacion = 0

                if self.reserva_habitacion == 'Ejecutiva Individual ($50.000)' :
                    precio_reserva_habitacion = 50000
                elif self.reserva_habitacion == 'Ejecutiva Doble ($80.000)':
                    precio_reserva_habitacion = 80000
                elif self.reserva_habitacion == 'Familiar ($150.000)':
                    precio_reserva_habitacion = 150000
                elif 'PentHouse' in self.reserva_habitacion:
                    precio_reserva_habitacion = 1080000

                precio_reserva_excursion = 0
                if self.reserva_excursion == 'Excursión Light ($5.000)' :
                    precio_reserva_excursion = 5000
                elif self.reserva_excursion == 'Excursión Plus ($25.000)':
                    precio_reserva_excursion = 25000
                elif self.reserva_excursion == 'Excursión Heavy ($50.000)':
                    precio_reserva_excursion = 50000
                
 
                precio_reserva_restaurante = 0
                if self.reserva_restaurante == 'Inicial ($10.000)' :
                    precio_reserva_restaurante = 10000
                elif self.reserva_restaurante == 'Intermedio ($25.000)':
                    precio_reserva_restaurante = 25000
                elif self.reserva_restaurante == 'Completo ($45.000)':
                    precio_reserva_restaurante = 45000
                elif self.reserva_restaurante == 'Avanzado ($60.000)':
                    precio_reserva_restaurante = 60000
                elif self.reserva_restaurante == 'Premium ($100.000)':
                    precio_reserva_restaurante = 100000
                    
                
                costo_total = precio_reserva_habitacion * self.diferencia_dias() + precio_reserva_restaurante + precio_reserva_excursion
                costo_total_str = "${:,.0f}".format(costo_total).replace(",", ".")
                linea_nueva = f"'{self.nombre}', 'Habitación: {self.reserva_habitacion} | Excursión: {self.reserva_excursion} | Restaurante: {self.reserva_restaurante}', '{self.inicio_fecha.date().toString('dd/MM/yyyy')}', '{self.final_fecha.date().toString('dd/MM/yyyy')}','{self.diferencia_dias()}','{costo_total_str}'\n"
                self.modificar_linea(self.linea_tabla, linea_nueva) 

                QMessageBox.information(self, "Reserva Exitosa", "Se ha actualizado la reserva")
                
                self.mi_signal.emit()
                self.input_nombre.clear()
                self.close()

            except Exception as e:
                print(f'El archivo no se encuentra ... {e}')

        else:
            QMessageBox.warning(self, "Error", "Verifique que la fecha de inicio y final sean correctas") 
   
    #obtiene la difencia de dias para calcular los días de estadía 
    def diferencia_dias(self):
        inicio = self.inicio_fecha.date()
        final = self.final_fecha.date()

        if inicio.isValid() and final.isValid():
            diferencia = inicio.daysTo(final)
            return diferencia
        
    #sobreescribe una linea en el archivo csv, la nueva  linea se pasa como parametro
    #junto con el indice de la linea que se quiere modificar
    def modificar_linea(self, linea_index, nueva_linea):
        with open('sprint-3\\archivo_reservas.csv', 'r') as file:
            lineas = file.readlines()

        if linea_index < 0 or linea_index >= len(lineas):
            print("Índice de línea inválido", linea_index, len(lineas))
            return

        lineas[linea_index] = nueva_linea

        with open('sprint-3\\archivo_reservas.csv', 'w') as file:
            file.writelines(lineas)

        
    
        