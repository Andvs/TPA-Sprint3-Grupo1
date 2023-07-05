import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidget, QHeaderView, QHBoxLayout, QTableWidgetItem
from PyQt6.QtGui import QAction
from reserva_interfaz import ReservaInterfaz
from agencia_turismo_interfaz import AgenciaTurismoInterfaz
from restaurante_interfaz import RestauranteInterfaz
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Reservas de Hotel")
        self.setFixedSize(450, 300)
        
        self.menus()

        widget = QWidget()
        layout = QHBoxLayout()
        self.table = QTableWidget(0, 4)  

        #tabla

        self.table.setHorizontalHeaderLabels(["Nombre", "Sección","Reserva", "Costo"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        layout.addWidget(self.table)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.cargar_datos()

    
    def menus(self):
        # Menú Reserva
        menu_reserva = self.menuBar().addMenu("Reserva")
        
        action_reserva = QAction("Reservar Habitación", self)
        action_reserva.triggered.connect(self.reserva)
        menu_reserva.addAction(action_reserva)
        
        # Menú Agencia de Turismo
        menu_agencia_turismo = self.menuBar().addMenu("Agencia de Turismo")
        
        action_agencia_turismo = QAction("Reservar Excursión", self)
        action_agencia_turismo.triggered.connect(self.agencia_turismo)
        menu_agencia_turismo.addAction(action_agencia_turismo)
        
        # Menú Restaurante
        menu_restaurante = self.menuBar().addMenu("Restaurante")
        
        action_restaurante = QAction("Hacer Pedido", self)
        action_restaurante.triggered.connect(self.restaurante)
        menu_restaurante.addAction(action_restaurante)
    
    def reserva(self):
        self.reserva_interface = ReservaInterfaz()
        self.reserva_interface.mi_signal.connect(self.agregar_reserva_tabla_reserva)
        self.reserva_interface.mi_signal.connect(self.cargar_datos)

        # Muestra la interfaz de reserva
        self.reserva_interface.show()
    
    def agencia_turismo(self):
        self.agencia_turismo_interface = AgenciaTurismoInterfaz()
        self.agencia_turismo_interface.mi_signal.connect(self.agregar_reserva_tabla_turismo)
        self.agencia_turismo_interface.mi_signal.connect(self.cargar_datos)

        # Muestra la interfaz de la agencia de turismo
        self.agencia_turismo_interface.show()
    
    def restaurante(self):
        self.restaurante_interface = RestauranteInterfaz()
        self.restaurante_interface.mi_signal.connect(self.agregar_reserva_tabla_restaurante)
        self.restaurante_interface.mi_signal.connect(self.cargar_datos)
        # Muestra la interfaz del restaurante
        self.restaurante_interface.show()

    def agregar_reserva_tabla_turismo(self):

        nombre_item = QTableWidgetItem(self.agencia_turismo_interface.nombre)
        nombre_item.setFlags(nombre_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        seccion_reserva_item = QTableWidgetItem(self.agencia_turismo_interface.seccion)
        seccion_reserva_item.setFlags(nombre_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        reserva_item = QTableWidgetItem(self.agencia_turismo_interface.seccion)
        reserva_item.setFlags(nombre_item.flags() & ~Qt.ItemFlag.ItemIsEditable)

        row_count = self.table.rowCount()
        self.table.insertRow(row_count)
        self.table.setItem(row_count, 0, nombre_item)
        self.table.setItem(row_count, 1, seccion_reserva_item)
        self.table.setItem(row_count, 2, reserva_item)

    def agregar_reserva_tabla_reserva(self):

        nombre_item = QTableWidgetItem(self.reserva_interface.nombre)
        nombre_item.setFlags(nombre_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        seccion_reserva_item = QTableWidgetItem(self.reserva_interface.seccion)
        seccion_reserva_item.setFlags(nombre_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        reserva_item = QTableWidgetItem(self.reserva_interface.tipo)
        reserva_item.setFlags(nombre_item.flags() & ~Qt.ItemFlag.ItemIsEditable)

        row_count = self.table.rowCount()
        self.table.insertRow(row_count)
        self.table.setItem(row_count, 0, nombre_item)
        self.table.setItem(row_count, 1, seccion_reserva_item)
        self.table.setItem(row_count, 2, reserva_item)

    def agregar_reserva_tabla_restaurante(self):

        nombre_item = QTableWidgetItem(self.restaurante_interface.nombre)
        nombre_item.setFlags(nombre_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        seccion_reserva_item = QTableWidgetItem(self.restaurante_interface.seccion)
        seccion_reserva_item.setFlags(nombre_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        reserva_item = QTableWidgetItem(self.restaurante_interface.tipo)
        reserva_item.setFlags(nombre_item.flags() & ~Qt.ItemFlag.ItemIsEditable)

        row_count = self.table.rowCount()
        self.table.insertRow(row_count)
        self.table.setItem(row_count, 0, nombre_item)
        self.table.setItem(row_count, 1, seccion_reserva_item)
        self.table.setItem(row_count, 2, reserva_item)

    def cargar_datos(self):
        self.table.clearContents()
        self.table.setRowCount(0)

        archivo_csv = open('sprint-3\\archivo_reservas.csv', 'r')

        for linea in archivo_csv:
            valores = linea.strip().split(',')

            row_count = self.table.rowCount()
            self.table.insertRow(row_count)

            for column, valor in enumerate(valores):
                item = QTableWidgetItem(valor.replace("'", ""))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(row_count, column, item)

        archivo_csv.close()


        

    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    main_window = MainWindow()
    main_window.show()
    
    sys.exit(app.exec())
