from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

class Base(DeclarativeBase):  
    pass

class BaseModel: 
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    def to_dict(self):  
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}