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

# USER MANAGEMENT
class UserRole(Base):

    __tablename__ = "user_role"

    id = Column(Integer, primary_key=True)
    code = Column(String(25))
    description = Column(String(255), nullable=False)


class Permission(Base):

    __tablename__ = "permission"

    id = Column(Integer, primary_key=True)
    code = Column(String(25))
    description = Column(String(255), nullable=False)

class RolePermission(Base):

    __tablename__ = "role_permission"

    id = Column(Integer, primary_key=True)
    role_id = Column(Integer, ForeignKey("user_role.id", ondelete="CASCADE"))
    permission_id = Column(Integer, ForeignKey("permission.id", ondelete="CASCADE"))


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    firstname = Column(String(100), nullable=False)
    middlename = Column(String(100))
    lastname = Column(String(100), nullable=False)

    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    role_id = Column(Integer, ForeignKey("user_role.id", ondelete="CASCADE"))


# References
class SoilQuality(Base):

    __tablename__ = "rf_soil_quality"

    id = Column(Integer, primary_key=True)
    code = Column(String(25))
    description = Column(String(255), nullable=False)


class SoilType(Base):
    __tablename__ = "rf_soil_type"

    id = Column(Integer, primary_key=True)
    code = Column(String(25))
    description = Column(String(255), nullable=False)

class IrrigationSource(Base):

    __tablename__ = "rf_irrigation_source"

    id = Column(Integer, primary_key=True)
    code = Column(String(25))
    description = Column(String(255), nullable=False)

class EnvironmentalFactor(Base):

    __tablename__ = "rf_environmental_factor"

    id = Column(Integer, primary_key=True)
    code = Column(String(25))
    description = Column(String(255), nullable=False)

class AccessToInputs(Base):

    __tablename__ = "rf_access_to_inputs"

    id = Column(Integer, primary_key=True)
    code = Column(String(25))
    description = Column(String(255), nullable=False)

class InputSource(Base):

    __tablename__ = "rf_input_source"

    id = Column(Integer, primary_key=True)
    code = Column(String(25))
    description = Column(String(255), nullable=False)

class Variety(Base):

    __tablename__ = "rf_variety"

    id = Column(Integer, primary_key=True)
    code = Column(String(25))
    description = Column(String(255), nullable=False)

class PlantingMethod(Base):

    __tablename__ = "rf_planting_method"

    id = Column(Integer, primary_key=True)
    code = Column(String(25))
    description = Column(String(255), nullable=False)

class PlantingDistance(Base):

    __tablename__ = "rf_planting_distance"

    id = Column(Integer, primary_key=True)
    code = Column(String(25))
    description = Column(String(255), nullable=False)

class IntercropCrops(Base):

    __tablename__ = "rf_intercrop_crops"

    id = Column(Integer, primary_key=True)
    code = Column(String(25))
    description = Column(String(255), nullable=False)


class PestType(Base):

    __tablename__ = "rf_pest_type"

    id = Column(Integer, primary_key=True)
    code = Column(String(25))
    description = Column(String(255), nullable=False)

class PestImpact(Base):

    __tablename__ = "rf_pest_impact"

    id = Column(Integer, primary_key=True)
    code = Column(String(25))
    description = Column(String(255), nullable=False)

class ControlMethod(Base):  

    __tablename__ = "rf_control_method"

    id = Column(Integer, primary_key=True)
    code = Column(String(25))
    description = Column(String(255), nullable=False)

class ControlFrequency(Base):

    __tablename__ = "rf_control_frequency"

    id = Column(Integer, primary_key=True)
    code = Column(String(25))
    description = Column(String(255), nullable=False)

class SoilTesting(Base):

    __tablename__ = "rf_soil_testing"

    id = Column(Integer, primary_key=True)
    code = Column(String(25))
    description = Column(String(255), nullable=False)

class TestingFrequency(Base):

    __tablename__ = "rf_testing_frequency"

    id = Column(Integer, primary_key=True)
    code = Column(String(25))
    description = Column(String(255), nullable=False)

class SoilConservation(Base):

    __tablename__ = "rf_soil_conservation"

    id = Column(Integer, primary_key=True)
    code = Column(String(25))
    description = Column(String(255), nullable=False)

class ConservationTechniques(Base):

    __tablename__ = "rf_conservation_techniques"

    id = Column(Integer, primary_key=True)
    code = Column(String(25))
    description = Column(String(255), nullable=False)

class SeasonalEffects(Base):

    __tablename__ = "rf_seasonal_effects"

    id = Column(Integer, primary_key=True)
    code = Column(String(25))
    description = Column(String(255), nullable=False)


# TRANSACIONS
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
    soil_quality_id = Column(Integer, ForeignKey("rf_soil_quality.id", ondelete="CASCADE"))
    soil_type_id = Column(Integer, ForeignKey("rf_soil_type.id", ondelete="CASCADE"))
    irrigation_source_id = Column(Integer, ForeignKey("rf_irrigation_source.id", ondelete="CASCADE"))
    environmental_factor_id = Column(Integer, ForeignKey("rf_environmental_factor.id", ondelete="CASCADE"))
    access_to_inputs_id = Column(Integer, ForeignKey("rf_access_to_inputs.id", ondelete="CASCADE"))
    input_source_id = Column(Integer, ForeignKey("rf_input_source.id", ondelete="CASCADE"))

    farm_area = Column(Float)
    average_yield = Column(Float)

class AbacaCultivation(Base):

    __tablename__ = "abaca_cultivation"

    id = Column(Integer, primary_key=True)
    farm_id = Column(Integer, ForeignKey("farms.id", ondelete="CASCADE"))
    variety_id = Column(Integer, ForeignKey("rf_variety.id", ondelete="CASCADE"))
    planting_distance_id = Column(Integer, ForeignKey("rf_planting_distance.id", ondelete="CASCADE"))
    planting_method_id = Column(Integer, ForeignKey("rf_planting_method.id", ondelete="CASCADE"))
    intercrop_crops_id = Column(Integer, ForeignKey("rf_intercrop_crops.id", ondelete="CASCADE"))

    year_first_planted = Column(Integer)
    abaca_area = Column(Float)
    intercropping = Column(String(255))

class PestManagement(Base):

    __tablename__ = "pest_management"

    id = Column(Integer, primary_key=True)
    abaca_id = Column(Integer, ForeignKey("abaca_cultivation.id", ondelete="CASCADE"))
    pest_type_id = Column(Integer, ForeignKey("rf_pest_type.id", ondelete="CASCADE"))
    pest_impact_id = Column(Integer, ForeignKey("rf_pest_impact.id", ondelete="CASCADE"))
    control_method_id = Column(Integer, ForeignKey("rf_control_method.id", ondelete="CASCADE"))
    control_frequency_id = Column(Integer, ForeignKey("rf_control_frequency.id", ondelete="CASCADE"))

class SoilManagement(Base):

    __tablename__ = "soil_management"

    id = Column(Integer, primary_key=True)
    farm_id = Column(Integer, ForeignKey("farms.id", ondelete="CASCADE"))

    soil_testing_id = Column(Integer, ForeignKey("rf_soil_testing.id", ondelete="CASCADE"))
    testing_frequency_id = Column(Integer, ForeignKey("rf_testing_frequency.id", ondelete="CASCADE"))
    soil_conservation_id = Column(Integer, ForeignKey("rf_soil_conservation.id", ondelete="CASCADE"))
    conservation_techniques_id = Column(Integer, ForeignKey("rf_conservation_techniques.id", ondelete="CASCADE"))
    seasonal_effects_id = Column(Integer, ForeignKey("rf_seasonal_effects.id", ondelete="CASCADE"))
    fertility_improvement = Column(String(255))

# CREATE TABLES
Base.metadata.create_all(engine)

# SESSION
Session = sessionmaker(bind=engine)
session = Session()