from services.file_loader import FileLoader
from services.database import DatabaseManager
from utils.logger import Logger

def main():
    logger = Logger()  
    db_manager = DatabaseManager()  
    
    try:
        db_manager.initialize_db()  
        
        loader = FileLoader(db_manager)  
        results = loader.load_files_from_directory('files')  
        
        
        for result in results:
            if result['success']:
                logger.log(f"✅ {result['filename']}: {result['records']} registros cargados")
            else:
                logger.log(f"❌ {result['filename']}: Error - {result['error']}")
    except Exception as e:
        logger.log(f"Error en la ejecución: {str(e)}")
    finally:
        db_manager.close_connection()  

if __name__ == "__main__":
    main()