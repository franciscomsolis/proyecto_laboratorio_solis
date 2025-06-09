from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base

class DatabaseManager:
    __instance = None  
    
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
    
    def initialize_db(self, db_url="sqlite:///laboratorio.db"):
        self.engine = create_engine(db_url)  
        self.Session = sessionmaker(bind=self.engine)  
        Base.metadata.create_all(self.engine)  
        
    def get_session(self):
        return self.Session()  
    
    def close_connection(self):
        if self.engine:
            self.engine.dispose()  