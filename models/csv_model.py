from models.base import Base, BaseModel
from sqlalchemy import Column, String, Float, Integer

class Producto(Base, BaseModel):
    __tablename__ = "productos"  
    
    nombre = Column(String(100), nullable=False)  
    categoria = Column(String(50))  
    precio = Column(Float, nullable=False) 
    stock = Column(Integer, nullable=False)  