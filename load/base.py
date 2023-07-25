from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Declaramos el motor de base de datos a usar
engine = create_engine('mssql+pyodbc://@(localdb)\\MSSQLLocalDB/PROYECTOBASE?driver=ODBC+Driver+17+for+SQL+Server')

Session = sessionmaker(bind=engine)

Base = declarative_base()
