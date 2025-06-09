import pandas as pd
from datetime import datetime

class DataValidator:
    def __init__(self, data):
        self.data = data.copy()
        
    def remove_duplicates(self, subset=None):
        self.data = self.data.drop_duplicates(subset=subset)
        
    def remove_null_values(self, required_columns):
        for col in required_columns:
            if col in self.data.columns:
                self.data = self.data.dropna(subset=[col])
                
    def validate_types(self, type_map):
        for col, expected_type in type_map.items():
            if col in self.data.columns:
                if expected_type == str:
                    self.data[col] = self.data[col].astype(str)
                elif expected_type == int:
                    self.data[col] = pd.to_numeric(self.data[col], errors='coerce').astype('Int64')
                elif expected_type == float:
                    self.data[col] = pd.to_numeric(self.data[col], errors='coerce')
                elif expected_type == "date":
                    self.data[col] = pd.to_datetime(self.data[col], errors='coerce')
                elif expected_type == "boolean":
                    self.data[col] = self.data[col].map({'SI': True, 'NO': False, 'Sí': True, 'No': False})
                    
    def convert_to_date(self, column, format='%Y-%m-%d'):
        if column in self.data.columns:
            self.data[column] = pd.to_datetime(self.data[column], format=format, errors='coerce')
            
    def get_clean_data(self):
        
        return self.data.dropna(how='all')
                