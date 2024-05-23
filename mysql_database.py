
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# Connection to the database
DATABASE_URL = "mysql+pymysql://apiuser:api123456@localhost:3306/apischema"  # TODO: send to .env file
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
