from models.base import Base, BaseModel
from sqlalchemy import Column, String, Date

class Cliente(Base, BaseModel):
    __tablename__ = "clientes"
    
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)  
    fecha_nacimiento = Column(Date)  
    telefono = Column(String(20)) 