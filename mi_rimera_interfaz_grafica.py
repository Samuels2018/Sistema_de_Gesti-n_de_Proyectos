from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from primer_programa_con_sqlalchelmi import Base

class DatabaseHandler:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseHandler, cls).__new__(cls)
            cls._instance.engine = create_engine('sqlite:///gestion_proyecto.db')
            cls._instance.Session = sessionmaker(bind=cls._instance.engine)
        return cls._instance

    def inicializar_db(self):
        Base.metadata.create_all(self.engine)

    # --- MÉTODOS DE LECTURA ---

    def consultar(self, modelo, filtro=None):
        """
        Obtiene registros de la base de datos.
        :para modelo: La clase de la tabla (ej. Usuario, Proyecto)
        :para filtro: Un diccionario opcional para filtrar (ej. {"nombre": "Juan"})
        :return: Lista de objetos encontrados
        """
        session = self.Session()
        try:
            query = session.query(modelo)
            
            if filtro:
                # Aplicar filtros dinámicamente basados en el diccionario
                for columna, valor in filtro.items():
                    query = query.filter(getattr(modelo, columna) == valor)
            
            resultados = query.all()
            return resultados
        except Exception as e:
            print(f"Error al consultar {modelo.__name__}: {e}")
            return []
        finally:
            session.close()

    # --- MÉTODOS DE ESCRITURA (DRY) ---

    def _ejecutar_accion(self, objeto, accion):
        session = self.Session()
        try:
            if accion == "guardar":
                session.merge(objeto)
            elif accion == "eliminar":
                objeto = session.merge(objeto)
                session.delete(objeto)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error en {accion}: {e}")
        finally:
            session.close()

    def insertar(self, objeto):
        self._ejecutar_accion(objeto, "guardar")

    def actualizar(self, objeto):
        self._ejecutar_accion(objeto, "guardar")

    def eliminar(self, objeto):
        self._ejecutar_accion(objeto, "eliminar")

    


                

       
             

       
               
      
           


    
    
   
   
   



   
    
  
   









    
    
    



