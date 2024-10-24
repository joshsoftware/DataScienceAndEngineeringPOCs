from langchain_community.document_loaders import SQLDatabaseLoader
from langchain_community.utilities import SQLDatabase
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class SimpleDBLoader:
    def __init__(self):
        # Set up database connection URI from environment variables
        db_type = os.getenv("DB_TYPE")
        host = os.getenv("DB_HOST")
        port = os.getenv("DB_PORT")
        database = os.getenv("DB_NAME")
        username = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")

        if db_type == "postgresql":
            self.uri = f"postgresql://{username}:{password}@{host}:{port}/{database}"
        elif db_type == "mysql":
            self.uri = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
        else:
            raise ValueError("Unsupported database type. Use 'postgresql' or 'mysql'")
        # Create database connection
        self.db = SQLDatabase.from_uri(self.uri)
    
    def load_data(self, query):
        """Load data using a custom query"""
        loader = SQLDatabaseLoader(
            db=self.db,
            query=query
        )
        return loader.load()

    def get_tables(self):
        """Get list of tables in the database"""
        return self.db.get_table_names()
    
    def close_connection(self):
        """Close the database connection"""
        self.db.close()

# Example usage for PostgreSQL
if __name__ == "__main__":
    # PostgreSQL Example
    postgres_loader = SimpleDBLoader()  
    # Show available tables
    print("Available tables:", postgres_loader.get_tables()) 
    table_names = postgres_loader.get_tables()
    for i in table_names:
        query = "SELECT * FROM " + i
        try:
            # Load data
            docs = postgres_loader.load_data(query)
            print(f"\nLoaded {len(docs)} documents") 
            # Print first document content
            if docs:
                print("\nFirst document content:")
                print(docs)      
        except Exception as e:
            print(f"Error loading data: {str(e)}")
