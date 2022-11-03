from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///./erp.db", connect_args={"check_same_thread": False})

sessionlocal = sessionmaker(bind=engine, autoflush=True, autocommit=False)

Base = declarative_base()


def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()
