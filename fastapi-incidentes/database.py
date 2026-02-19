from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Cambia usuario y contraseña por los tuyos
URL_DATABASE = "mysql+pymysql://root:@127.0.0.1:3310/fastapi_incidentes"

engine = create_engine(URL_DATABASE)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()