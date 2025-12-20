from sqlalchemy import (Column,
Integer,String,ForeignKey,Date,Float,create_engine)
from sqlalchemy.orm import relationship,declarative_base

# Funcion de la libreria sqlalchemy.orm para crear una clase dato para modelos de datos

Base = declarative_base()

# Representa la entidad principal del sistema donde se almacena la informacion  primordial del proyecto.
  
class Proyecto(Base):
    __tablename__='proyecto'
    id = Column(Integer,primary_key = True)
    nombre = Column(String(100),nullable = False)
    descripcion = Column(String(255))
    fecha_inicio = Column(Date)
    fecha_fin = Column(Date)
    estado = Column(String(50))
    tareas = relationship("tareas",back_populates="proyecto")
    
# Define las tareas espeficicas a realizar de un proyecto mediante una clave foranea  

class Tarea(Base):
    __tablename__='tareas'    
    id = Column(Integer,primary_key = True)
    proyecto_id = Column(Integer,ForeignKey ('proyecto.id'))
    nombre  = Column(String(100))
    descripcion  = Column(String(255))
    prioridad = Column(String(20))
    fecha_inicio = Column(Date)
    fecha_fin = Column(Date)
    proyecto = relationship("proyecto",back_populates="tareas")

# Almacena los datos de los usuarios y sus horas disponibles para realizar las tareas    

class Usuario(Base):
    __tablename__='usuarios'    
    id = Column(Integer,primary_key = True)    
    nombre  = Column(String(100))
    email  = Column(String(255))
    rol = Column(String(20))
    horas_disponibles = Column(Date)

""" Tabla intermedia utilizada para la union de dos tablas principales(tareas y usuarios),
donde se les asignara tareas y horas para realizarlos """
     

class Asignacion(Base):
    __tablename__='asignaciones'    
    tarea_id = Column(Integer,ForeignKey('tareas.id'),primary_key = True)
    usuario_id = Column(Integer,ForeignKey('usuarios.id'),primary_key = True)  
    horas_asignadas  = Column(Float)

""" Registra el historial del campo real trabajado por un usuario en una tarea,permitiendo el
control de horas y fecha."""

class TimeTracking(Base):
    __tablename__='time_tracking'    
    tarea_id = Column(Integer,ForeignKey('tareas.id'),primary_key = True)
    usuario_id = Column(Integer,ForeignKey('usuarios.id'),primary_key = True)  
    fecha  = Column(Date)
    horas  = Column(Float)
    tareas = relationship("proyecto",back_populates="tareas")
    
    
    
    
      





































































