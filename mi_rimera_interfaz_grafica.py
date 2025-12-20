from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date 
from primer_programa_con_sqlalchelmi import Base,Proyecto,Tarea,Usuario,Asignacion,TimeTracking

# Motor del programa 
class DatabaseHandler:

# Configura la conexion a la base de datos SQLITE y prepara la fabrica de sesiones para las transacciones
    def __init__(self):
        self.engine = create_engine('sqlite:///gestion_proyecto.db')
        self.Session = sessionmaker(bind = self.engine)

# Crea fisicamente todas las tablas definidas en los modelos dentro del archivo.db si aun no existen

    def inicializar_db(self):
        Base.metadata.create_all(self.engine)


    def insertar(self,objeto):
        session = self.Session()

        try:
            session.add(objeto)
            session.commit()
            print(f"Registro{type(objeto).__name__} insertado correctamente: ")               

        except Exception as e:
                    session.rollback()
                    print(f"Error al insertar: {e}")
                 
        finally:
                session.close()
        
 # Toma un registro exixtente que ha sido modificado y sincroniza los cambios con la base de datos   

    def actualizar(self,objeto):
        session = self.Session()

        try:
             session.add(objeto)
             session.commit()
             print(f"Registro{type(objeto).__name__} actualizado correctamente: ")

        except Exception as e:
               session.rollback()
               print(f"Error al actualizar: {e}")

        finally:
            session.close()

# Borra de forma segura un registroespecifico de la tabla correspondiente

    def eliminar(self,objeto): 
            session = self.Session()

            try:
                session.delete(objeto)
                session.commit()
                print(f"Registro{type(objeto).__name__} eliminado correctamente: ")


            except Exception as e:

                session.rollback()
                print(f"Error al eliminar: {e}")


            finally:

                 session.close()

    
""" Recibe un objeto de cualquier modelo y lo guarda permanemente en la base de datos,manejando errores
con un sistema de rollback. """

def leer(self,clase_modelo): 
            session = self.Session()

            try:
                registros = session.query(clase_modelo).all()
                return registros

            except Exception as e:

                session.rollback()
                print(f"Error al leer: {e}")
                return []

            finally:

                 session.close()



                

       
             

       
               
      
           


    
    
   
   
   



   
    
  
   









    
    
    



