import sys
from PyQt5 import QtWidgets, uic, QtCore
# Asegúrate de que el nombre del archivo de tus modelos sea el correcto
from mi_rimera_interfaz_grafica import DatabaseHandler, Proyecto, Tarea, Usuario, Asignacion, TimeTracking 

class MiVentanaPrincipal(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Carga la interfaz sin necesidad de abrir QtDesigner
        uic.loadUi("ventana.ui", self)
        
        # Inicializar conexión a la base de datos
        self.db = DatabaseHandler()
        self.db.inicializar_db()

        # --- CONEXIÓN DE BOTONES LATERALES (Cambio de Pestañas) ---
        # Usamos try/except por si algún nombre de botón en el UI varía
        buttons_mapping = {
            "Proyecto": 0,
            "Tarea": 1,
            "Usuario": 2,
            "Asignacion": 3,
            "TimeTracking": 4
        }
        
        for btn_name, index in buttons_mapping.items():
            btn = getattr(self, btn_name, None)
            if btn:
                btn.clicked.connect(lambda _, idx=index: self.stackedWidget.setCurrentIndex(idx))

        # --- CONEXIÓN DE BOTONES DE ACCIÓN ---
        self.insertar.clicked.connect(self.guardar_en_base_de_datos)
        self.leer.clicked.connect(self.cargar_datos_en_tablas)
        self.eliminar.clicked.connect(self.eliminar_general)
        self.actualizar.clicked.connect(self.actualizar_general)

    def obtener_tabla_actual(self):
        """Encuentra la tabla QTableWidget dentro de la pestaña activa del stackedWidget."""
        pestaña_actual = self.stackedWidget.currentWidget()
        tabla = pestaña_actual.findChild(QtWidgets.QTableWidget)
        return tabla

    def cargar_datos_en_tablas(self):
        """Lee los datos de la DB y los muestra en la tabla con sus columnas reales."""
        idx = self.stackedWidget.currentIndex()
        tabla = self.obtener_tabla_actual()

        if not tabla:
            QtWidgets.QMessageBox.warning(self, "Aviso", "No se encontró un objeto Tabla en esta pestaña.")
            return

        # 1. Configuración de Modelos y Columnas Reales
        # Estructura: { índice: (Modelo, [Nombres de Columnas]) }
        config = {
            0: (Proyecto, ["ID", "Nombre", "Descripción", "Estado"]),
            1: (Tarea, ["ID", "Nombre Tarea", "Proyecto ID", "Prioridad"]),
            2: (Usuario, ["ID", "Nombre", "Email", "Rol"]),
            3: (Asignacion, ["ID Tarea", "ID Usuario", "Horas Asignadas"]),
            4: (TimeTracking, ["ID", "ID Tarea", "ID Usuario", "Horas Reales", "Fecha"])
        }

        modelo_clase, nombres_columnas = config.get(idx, (None, []))
        if not modelo_clase: return

        # Leer registros
        registros = self.db.leer(modelo_clase)
        
        # Preparar la tabla UI
        tabla.setColumnCount(len(nombres_columnas))
        tabla.setHorizontalHeaderLabels(nombres_columnas)
        tabla.setRowCount(0)

        # 2. Llenado de filas según el modelo
        for i, reg in enumerate(registros):
            tabla.insertRow(i)
            
            if idx == 0: # Proyecto
                datos = [reg.id, reg.nombre, reg.descripcion, getattr(reg, 'estado', 'Activo')]
            elif idx == 1: # Tarea
                datos = [reg.id, reg.nombre, reg.proyecto_id, getattr(reg, 'prioridad', 'Normal')]
            elif idx == 2: # Usuario
                datos = [reg.id, reg.nombre, reg.email, getattr(reg, 'rol', 'Miembro')]
            elif idx == 3: # Asignacion
                datos = [reg.tarea_id, reg.usuario_id, reg.horas_asignadas]
            elif idx == 4: # TimeTracking
                datos = [reg.id, reg.tarea_id, reg.usuario_id, reg.horas_reales, str(reg.fecha)]
            else:
                datos = []

            for j, valor in enumerate(datos):
                item = QtWidgets.QTableWidgetItem(str(valor))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                tabla.setItem(i, j, item)
        
        # Estética: Ajustar columnas al ancho de la ventana
        tabla.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

    def guardar_en_base_de_datos(self):
        """Toma los textos de los inputs y crea el objeto correspondiente en la DB."""
        idx = self.stackedWidget.currentIndex()
        try:
            nuevo_objeto = None
            
            if idx == 0: # Proyecto
                nuevo_objeto = Proyecto(nombre=self.txt_nom.text(), descripcion=self.txt_desc.text())
            elif idx == 1: # Tarea
                nuevo_objeto = Tarea(nombre=self.txt_nom_t.text(), proyecto_id=int(self.txt_id_p.text()))
            elif idx == 2: # Usuario
                nuevo_objeto = Usuario(nombre=self.txt_nom_u.text(), email=self.txt_email_u.text())
            elif idx == 3: # Asignacion
                nuevo_objeto = Asignacion(
                    tarea_id=int(self.input_tarea_id.text()), 
                    usuario_id=int(self.input_usuario_id.text()), 
                    horas_asignadas=float(self.input_horas.text())
                )
            elif idx == 4: # TimeTracking
                nuevo_objeto = TimeTracking(
                    tarea_id=int(self.txt_id_tarea_tt.text()), 
                    usuario_id=int(self.txt_id_user_tt.text()), 
                    horas_reales=float(self.txt_horas_tt.text())
                )

            if nuevo_objeto:
                self.db.insertar(nuevo_objeto)
                QtWidgets.QMessageBox.information(self, "Éxito", "Registro guardado correctamente.")
                self.cargar_datos_en_tablas() # Refrescar tabla
                self.limpiar_campos()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error de Datos", f"Verifica que los IDs sean números y los campos no estén vacíos.\nDetalle: {e}")

    def limpiar_campos(self):
        """Limpia todos los LineEdit de la interfaz."""
        for campo in self.findChildren(QtWidgets.QLineEdit):
            campo.clear()

    def eliminar_general(self):
        """Elimina la fila seleccionada de la base de datos."""
        tabla = self.obtener_tabla_actual()
        if not tabla or tabla.currentRow() == -1:
            QtWidgets.QMessageBox.warning(self, "Selección", "Por favor, selecciona una fila en la tabla.")
            return

        fila = tabla.currentRow()
        id_valor = tabla.item(fila, 0).text() # Asumimos que la col 0 siempre es el ID o la PK
        
        respuesta = QtWidgets.QMessageBox.question(self, "Confirmar", f"¿Seguro que deseas eliminar el registro con ID {id_valor}?",
                                                 QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        
        if respuesta == QtWidgets.QMessageBox.Yes:
            idx = self.stackedWidget.currentIndex()
            modelos = {0: Proyecto, 1: Tarea, 2: Usuario, 3: Asignacion, 4: TimeTracking}
            modelo_clase = modelos[idx]
            
            # Buscamos el objeto en la DB para borrarlo
            registros = self.db.leer(modelo_clase)
            for r in registros:
                # Caso especial para Asignacion (que no tiene .id sino .tarea_id)
                identificador = getattr(r, 'id', getattr(r, 'tarea_id', None))
                if str(identificador) == id_valor:
                    self.db.eliminar(r)
                    break
            
            self.cargar_datos_en_tablas()

    def actualizar_general(self):
        """Muestra un aviso de que el registro fue seleccionado para edición."""
        QtWidgets.QMessageBox.information(self, "Actualizar", "Función de edición: Modifica los campos de texto y presiona Insertar (o implementa Update según tu modelo).")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # Estilo visual opcional
    app.setStyle("Fusion") 
    mi_programa = MiVentanaPrincipal()
    mi_programa.show()
    sys.exit(app.exec_())

