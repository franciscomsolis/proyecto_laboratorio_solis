import os
import pandas as pd
from services.validator import DataValidator
from services.database import DatabaseManager
from models.csv_model import Producto
from models.json_model import Cliente
from datetime import datetime

class FileLoader:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.validators = {
            'csv': self._validate_csv,
            'json': self._validate_json
        }
        self.mappers = {
            'csv': self._map_csv_to_model,
            'json': self._map_json_to_model
        }
        
    def load_files_from_directory(self, directory_path):
        results = []
        
        if not os.path.exists(directory_path):
            raise FileNotFoundError(f"El directorio {directory_path} no existe")
            
        for filename in os.listdir(directory_path):
            filepath = os.path.join(directory_path, filename)
            if os.path.isfile(filepath):
                result = self._process_file(filepath, filename)
                results.append(result)
                
        return results
        
    def _process_file(self, filepath, filename):
        try:
            file_ext = filename.split('.')[-1].lower()
            
            if file_ext not in self.validators:
                return {
                    'filename': filename,
                    'success': False,
                    'error': f"Formato {file_ext} no soportado",
                    'records': 0
                }
                
            # Leer archivo
            data = self._read_file(filepath, file_ext)
            
            # Validar datos
            validator = self.validators[file_ext]
            clean_data = validator(data)
            
            if clean_data.empty:
                return {
                    'filename': filename,
                    'success': False,
                    'error': "No hay datos válidos después de la validación",
                    'records': 0
                }
                
            # Mapear a modelo
            mapper = self.mappers[file_ext]
            records = mapper(clean_data)
            
            # Guardar en base de datos
            session = self.db_manager.get_session()
            session.add_all(records)
            session.commit()
            
            return {
                'filename': filename,
                'success': True,
                'error': None,
                'records': len(records)
            }
            
        except Exception as e:
            return {
                'filename': filename,
                'success': False,
                'error': str(e),
                'records': 0
            }
            
    def _read_file(self, filepath, file_ext):
        if file_ext == 'csv':
            return pd.read_csv(filepath)
        elif file_ext == 'json':
            return pd.read_json(filepath)
        else:
            raise ValueError(f"Extensión {file_ext} no soportada")
            
    def _validate_csv(self, data):
        validator = DataValidator(data)
        
        # Validaciones para CSV (Productos)
        validator.remove_duplicates()
        validator.remove_null_values(['nombre', 'precio', 'stock'])
        validator.validate_types({
            'nombre': str,
            'categoria': str,
            'precio': float,
            'stock': int
        })
        
        return validator.get_clean_data()
        
    def _validate_json(self, data):
        validator = DataValidator(data)
        
        # Validaciones para JSON (Clientes)
        validator.remove_duplicates(subset=['email'])
        validator.remove_null_values(['nombre', 'email'])
        validator.validate_types({
            'nombre': str,
            'email': str,
            'fecha_nacimiento': str,  # Se convierte a date después
            'telefono': str
        })
        
        # Convertir fecha
        if 'fecha_nacimiento' in validator.get_clean_data().columns:
            validator.convert_to_date('fecha_nacimiento', format='%Y-%m-%d')
            
        return validator.get_clean_data()
        
    def _map_csv_to_model(self, data):
        records = []
        for _, row in data.iterrows():
            record = Producto(
                nombre=row['nombre'],
                categoria=row.get('categoria'),
                precio=row['precio'],
                stock=row['stock']
            )
            records.append(record)
        return records
        
    def _map_json_to_model(self, data):
        records = []
        for _, row in data.iterrows():
            record = Cliente(
                nombre=row['nombre'],
                email=row['email'],
                fecha_nacimiento=row.get('fecha_nacimiento'),
                telefono=row.get('telefono')
            )
            records.append(record)
        return records