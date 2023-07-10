import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QTableWidget, QHeaderView, QTableWidgetItem, QMessageBox
from reserva_interfaz import ReservaInterfaz
from PyQt6.QtCore import Qt
from actualizaReservaInterfaz import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Reservas de Hotel")
        self.setFixedSize(950, 400)

        widget = QWidget()
        layout = QVBoxLayout()
        self.table = QTableWidget(0, 8)  

        button_reservar = QPushButton("Realizar Reserva")
        button_reservar.setFixedSize(250, 30)
        button_reservar.clicked.connect(self.reserva)
        layout.addWidget(button_reservar)

        #tabla

        self.table.setHorizontalHeaderLabels(["Nombre", "Reserva", "Inicio", "Fin" ,"Días", "Costo", "Actualizar", "Eliminar"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        

        layout.addWidget(self.table)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.cargar_datos_tabla()

    def reserva(self):
        self.reserva_interface = ReservaInterfaz()
        self.reserva_interface.mi_signal.connect(self.cargar_datos_tabla)
        self.reserva_interface.show()
    

    def cargar_datos_tabla(self):
        self.table.clearContents()
        self.table.setRowCount(0)

        archivo_csv = open('sprint-3\\archivo_reservas.csv', 'r')

        for linea in archivo_csv:
            valores = linea.strip().split(',')
            row_count = self.table.rowCount()
            self.table.insertRow(row_count)
            self.table.setRowHeight(row_count, 150)
            

            for column, valor in enumerate(valores):
                item = QTableWidgetItem(valor.replace("'", ""))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(row_count, column, item)

            
            actualizar_button = QPushButton('Actualizar')
            actualizar_button.clicked.connect(lambda: self.actualizar_reserva(self.table.currentRow()))
            self.table.setCellWidget(row_count, 6, actualizar_button)
                            
            delete_button = QPushButton('Eliminar')
            delete_button.clicked.connect(self.eliminar_reserva_seleccionada)
            self.table.setCellWidget(row_count, 7, delete_button)

            
            
        archivo_csv.close()

    
    def eliminar_reserva_seleccionada(self):

        confirmacion = QMessageBox.question(self, "Confirmación", "¿Estás seguro?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if confirmacion == QMessageBox.StandardButton.Yes:
            selected_row = self.table.currentRow()
            print(selected_row)
            if selected_row != -1:
                self.table.removeRow(selected_row)

            with open('sprint-3\\archivo_reservas.csv', 'r') as archivo_origen:
                lineas = archivo_origen.readlines()

            # Verifica que el número de línea sea válido
            if selected_row < 0 or selected_row >= len(lineas):
                print(selected_row)
                print("Número de línea inválido")
                return

            # Elimina la línea deseada de la lista de líneas
            del lineas[selected_row]

            with open('sprint-3\\archivo_reservas.csv', 'w') as archivo_destino:
                archivo_destino.writelines(lineas)

            QMessageBox.information(self, "Eliminar reserva", "Se ha eliminado exitosamente la reserva.")
    
        

    def actualizar_reserva(self, posicion):
        self.reserva_actualizar_interfaz = ActualizarReservaInterfaz(posicion)
        self.reserva_actualizar_interfaz.mi_signal.connect(self.cargar_datos_tabla)
        self.reserva_actualizar_interfaz.show()

        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    main_window = MainWindow()
    main_window.show()
    
    sys.exit(app.exec())
