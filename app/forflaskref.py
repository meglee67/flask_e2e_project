from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Load environment variables from .env file
load_dotenv()

# Database connection settings from environment variables
DB_HOST = os.getenv("DB_HOST")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_CHARSET = os.getenv("DB_CHARSET", "utf8mb4")

# Connection string
conn_string = (
    f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
    f"?charset={DB_CHARSET}"
)

Base = declarative_base()

# Medicine model
class Medicine(Base):
    __tablename__ = 'medicines'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    cost_covered = Column(Float, nullable=False)
    cost_not_covered = Column(Float, nullable=False)

# Insurance Provider model
class InsuranceProvider(Base):
    __tablename__ = 'insurance_providers'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

# Coverage model (Many-to-Many)
class Coverage(Base):
    __tablename__ = 'coverage'

    id = Column(Integer, primary_key=True)
    medicine_id = Column(Integer, ForeignKey('medicines.id'))
    provider_id = Column(Integer, ForeignKey('insurance_providers.id'))
    covered = Column(Boolean, nullable=False)
    price = Column(Float, nullable=False)

    # Relationships
    medicine = relationship('Medicine', backref='providers')
    provider = relationship('InsuranceProvider', backref='medicines')

# Establish database connection using the connection string
engine = create_engine(conn_string)

# Bind the engine to the Base class
Base.metadata.bind = engine

# Create a session
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create tables in the database
Base.metadata.create_all(engine)

# Close the session
session.close()