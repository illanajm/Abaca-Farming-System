from sqlalchemy import (
     create_engine,
    Column,
    Integer,
    String,
    Float,
    ForeignKey
)

from sqlalchemy.orm import declarative_base, sessionmaker

# =========================================
# MYSQL CONNECTION
# =========================================

USERNAME = "root"
PASSWORD = ""
HOST = "localhost"
DATABASE = "abaca_system"

DATABASE_URL = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}"

engine = create_engine(DATABASE_URL)

Base = declarative_base()

# =========================================
# USERS TABLE
# =========================================

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    firstname = Column(String(100), nullable=False)
    middlename = Column(String(100))
    lastname = Column(String(100), nullable=False)

    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)


class Farmer(Base):

    __tablename__ = "farmers"

    id = Column(Integer, primary_key=True)

    firstname = Column(String(100), nullable=False)
    middlename = Column(String(100))
    lastname = Column(String(100), nullable=False)

    sex = Column(String(10))
    birthdate = Column(String(20))
    age = Column(Integer)
    civil_status = Column(String(20))
    city_municipality = Column(String(100))
    barangay = Column(String(100))
    years_in_farming = Column(Integer)
    farming_break = Column(Integer)
    break_year_start = Column(Integer)
    break_year_end = Column(Integer)
    reason_for_break = Column(String(255), nullable=True)

class Farm(Base):

    __tablename__ = "farms"

    id = Column(Integer, primary_key=True)
    farmer_id = Column(Integer, ForeignKey("farmers.id", ondelete="CASCADE"))

    farm_area = Column(Float)
    soil_quality = Column(String(50))
    soil_type = Column(String(50))
    irrigation_source = Column(String(50))
    environmental_factors = Column(String(255))
    access_to_inputs = Column(String(255))
    input_source = Column(String(255))
    average_yield = Column(Float)

class AbacaCultivation(Base):

    __tablename__ = "abaca_cultivation"

    id = Column(Integer, primary_key=True)
    farm_id = Column(Integer, ForeignKey("farms.id", ondelete="CASCADE"))

    year_first_planted = Column(Integer)
    abaca_area = Column(Float)
    variety = Column(String(50))
    planting_distance = Column(String(50))
    planting_method = Column(String(50))
    intercropping = Column(String(255))
    intercrop_crops = Column(String(255))

class PestManagement(Base):

    __tablename__ = "pest_management"

    id = Column(Integer, primary_key=True)
    abaca_id = Column(Integer, ForeignKey("abaca_cultivation.id", ondelete="CASCADE"))

    pest_type = Column(String(255))
    pest_impact = Column(String(255))
    control_method = Column(String(255))
    control_frequency = Column(String(255))

class SoilManagement(Base):

    __tablename__ = "soil_management"

    id = Column(Integer, primary_key=True)
    farm_id = Column(Integer, ForeignKey("farms.id", ondelete="CASCADE"))

    soil_testing = Column(String(255))
    testing_frequency = Column(String(255))
    fertility_improvement = Column(String(255))
    soil_conservation = Column(String(255))
    conservation_techniques = Column(String(255))
    seasonal_effects = Column(String(255))

# CREATE TABLES
Base.metadata.create_all(engine)

# SESSION
Session = sessionmaker(bind=engine)
session = Session()