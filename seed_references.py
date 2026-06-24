from database import session
from database import (
    SoilQuality,
    SoilType,
    IrrigationSource,
    EnvironmentalFactor,
    AccessToInputs,
    InputSource,
    Variety,
    PlantingMethod,
    PlantingDistance,
    IntercropCrops,
    PestType,
    PestImpact,
    ControlMethod,
    ControlFrequency,
    SoilTesting,
    TestingFrequency,
    SoilConservation,
    ConservationTechniques,
    SeasonalEffects,
)

def seed_soil_quality():
    soil_quality = [
        ("Excellent", "Excellent"),
        ("Good", "Good"),
        ("Fair", "Fair"),
        ("Poor", "Poor"),
        ("Very Poor", "Very Poor")
    ]

    for code, desc in soil_quality:
        existing = session.query(SoilQuality).filter_by(code=code).first()
        if not existing:
            session.add(SoilQuality(code=code, description=desc))

    session.commit()

def seed_soil_type():
    soil_type = [
        ("Sandy", "Sandy"),
        ("Clay", "Clay"),
        ("Silty", "Silty"),
        ("Loamy", "Loamy"),
        ("Peaty", "Peaty"),
        ("Chalky", "Chalky"),
        ("Volcanic", "Volcanic"),
        ("Alluvial", "Alluvial")
    ]

    for code, desc in soil_type:
        existing = session.query(SoilType).filter_by(code=code).first()
        if not existing:
            session.add(SoilType(code=code, description=desc))

    session.commit()

def seed_irrigation_source():
    irrigation_source = [
        ("River/Stream", "River/Stream"),
        ("Rainfall", "Rainfall"),
        ("Irrigation System", "Irrigation System"),
        ("Deep Well", "Deep Well"),
        ("Shallow Well", "Shallow Well"),
        ("Spring", "Spring"),
        ("Farm Pond", "Farm Pond"),
        ("Rainwater Harvesting", "Rainwater Harvesting"),
        ("Multiple Sources", "Multiple Sources")
    ]

    for code, desc in irrigation_source:
        existing = session.query(IrrigationSource).filter_by(code=code).first()
        if not existing:
            session.add(IrrigationSource(code=code, description=desc))

    session.commit()

def seed_environmental_factor():
    environmental_factor = [
        ("Climate Change", "Climate Change"),
        ("Soil Degradation", "Soil Degradation"),
        ("Pest Infestations", "Pest Infestations"),
        ("Natural Disasters", "Natural Disasters"),
        ("Plant diseases", "Plant diseases")
    ]

    for code, desc in environmental_factor:
        existing = session.query(EnvironmentalFactor).filter_by(code=code).first()
        if not existing:
            session.add(EnvironmentalFactor(code=code, description=desc))

    session.commit()

def seed_access_to_input():
    access_to_input = [
        ("Yes", "Yes"),
        ("No", "No")
    ]

    for code, desc in access_to_input:
        existing = session.query(AccessToInputs).filter_by(code=code).first()
        if not existing:
            session.add(AccessToInputs(code=code, description=desc))

    session.commit()

def seed_input_source():
    input_source = [
        ("Government", "Government"),
        ("Private Supplier", "Private Supplier"),
        ("Farmers Cooperative", "Farmers Cooperative"),
        ("Neighboring Farmer", "Neighboring Farmer"),
        ("Own Production", "Own Production"),
        ("NGO Assistance", "NGO Assistance"),
        ("Research Institution", "Research Institution"),
        ("Market/Agri Supply Store", "Market/Agri Supply Store"),
        ("DA/LGU Program", "DA/LGU Program"),
        ("Agricultural Companies", "Agricultural Companies"),
        ("Farmer Groups", "Farmer Groups"),
        ("Local Suppliers", "Local Suppliers"),
        ("Others", "Others"),
        ("No Input Source", "No Input Source")
    ]

    for code, desc in input_source:
        existing = session.query(InputSource).filter_by(code=code).first()
        if not existing:
            session.add(InputSource(code=code, description=desc))

    session.commit()

def seed_variety():
    variety = [
        ("Inosa", "Inosa"),
        ("Nilawaan", "Nilawaan"),
        ("Enusa", "Enusa"),
        ("Tangongon", "Tangongon")
    ]

    for code, desc in variety:
        existing = session.query(Variety).filter_by(code=code).first()
        if not existing:
            session.add(Variety(code=code, description=desc))

    session.commit()

def seed_planting_method():
    planting_method = [
        ("Direct Planting", "Direct Planting"),
        ("Nursery-Grown seedlings", "Nursery-Grown seedlings")
    ]

    for code, desc in planting_method:
        existing = session.query(PlantingMethod).filter_by(code=code).first()
        if not existing:
            session.add(PlantingMethod(code=code, description=desc))

    session.commit()

def seed_planting_distance():
    planting_distance = [
        ("0.5 m", "0.5 m"),
        ("2 m", "2 m"),
        ("3 m", "3 m"),
        ("5 m", "5 m")
    ]

    for code, desc in planting_distance:
        existing = session.query(PlantingDistance).filter_by(code=code).first()
        if not existing:
            session.add(PlantingDistance(code=code, description=desc))

    session.commit()

def seed_intercrop_crops():
    intercrop_crops = [
        ("Camote", "Camote"),
        ("Peanut", "Peanut"),
        ("Cacao", "Cacao"),
        ("Casava", "Casava"),
        ("No Crops", "No Crops")
    ]

    for code, desc in intercrop_crops:
        existing = session.query(IntercropCrops).filter_by(code=code).first()
        if not existing:
            session.add(IntercropCrops(code=code, description=desc))

    session.commit()

def seed_pest_type():
    pest_type = [
        ("Root Borers", "Root Borers"),
        ("Aphids", "Aphids"),
        ("Mealy Bugs", "Mealy Bugs")
    ]

    for code, desc in pest_type:
        existing = session.query(PestType).filter_by(code=code).first()
        if not existing:
            session.add(PestType(code=code, description=desc))

    session.commit()

def seed_pest_impact():
    pest_impact = [
        ("Slower Plant Growth", "Slower Plant Growth"),
        ("Reduced quality of fibers", "Reduced quality of fibers"),
        ("Significant Yield Loss", "Significant Yield Loss")
    ]

    for code, desc in pest_impact:
        existing = session.query(PestImpact).filter_by(code=code).first()
        if not existing:
            session.add(PestImpact(code=code, description=desc))

    session.commit()

def seed_control_method():
    control_method = [
        ("Organic methods (e.g., neem oil, insecticidal soap)", "Organic methods (e.g., neem oil, insecticidal soap)"),
        ("Chemical Pesticides", "Chemical Pesticides"),
        ("Cultural Practices (e.g., Crop Rotation)", "Cultural Practices (e.g., Crop Rotation)"),
    ]

    for code, desc in control_method:
        existing = session.query(ControlMethod).filter_by(code=code).first()
        if not existing:
            session.add(ControlMethod(code=code, description=desc))

    session.commit()

def seed_control_frequency():
    control_frequency = [
        ("Daily", "Daily"),
        ("Monthly", "Monthly"),
        ("Weekly", "Weekly"),
        ("As Needed (When Pests Are Noticed)", "As Needed (When Pests Are Noticed)")
    ]

    for code, desc in control_frequency:
        existing = session.query(ControlFrequency).filter_by(code=code).first()
        if not existing:
            session.add(ControlFrequency(code=code, description=desc))

    session.commit()

def seed_soil_testing():
    soil_testing = [
        ("Yes", "Yes"),
        ("No", "No")
    ]

    for code, desc in soil_testing:
        existing = session.query(SoilTesting).filter_by(code=code).first()
        if not existing:
            session.add(SoilTesting(code=code, description=desc))

    session.commit()

def seed_testing_frequency():
    testing_frequency = [
        ("Daily", "Daily"),
        ("Weekly", "Weekly"),
        ("Bi-weekly", "Bi-weekly"),
        ("Monthly", "Monthly"),
        ("Quarterly", "Quarterly"),
        ("Semi-Annual", "Semi-Annual"),
        ("Annually", "Annually"),
        ("Before Planting Season", "Before Planting Season"),
        ("After Harvest", "After Harvest"),
        ("When Problems Occur", "When Problems Occur"),
        ("No Regular Testing", "No Regular Testing"),
        ("Every Few Years", "Every Few Years"),
        ("N/A", "N/A")
    ]

    for code, desc in testing_frequency:
        existing = session.query(TestingFrequency).filter_by(code=code).first()
        if not existing:
            session.add(TestingFrequency(code=code, description=desc))

    session.commit()

def seed_soil_conservation():
    soil_conservation = [
        ("Yes", "Yes"),
        ("No", "No")
    ]

    for code, desc in soil_conservation:
        existing = session.query(SoilConservation).filter_by(code=code).first()
        if not existing:
            session.add(SoilConservation(code=code, description=desc))

    session.commit()

def seed_conservation_techniques():
    conservation_techniques = [
        ("Contour Plowing", "Contour Plowing"),
        ("Water the Soil", "Water the Soil"),
        ("Crop Rotation", "Crop Rotation"),
        ("No-till Farming", "No-till Farming"),
        ("Cover Crops", "Cover Crops"),
        ("N/A", "N/A")
    ]

    for code, desc in conservation_techniques:
        existing = session.query(ConservationTechniques).filter_by(code=code).first()
        if not existing:
            session.add(ConservationTechniques(code=code, description=desc))

    session.commit()

def seed_seasonal_effects():
    seasonal_effects = [
        ("Soil fertility improvement due to seasonal rains", "Soil fertility improvement due to seasonal rains"),
        ("Soil compaction during the dry season", "Soil compaction during the dry season"),
        ("Increased soil erosion during the rainy season", "Increased soil erosion during the rainy season")
    ]

    for code, desc in seasonal_effects:
        existing = session.query(SeasonalEffects).filter_by(code=code).first()
        if not existing:
            session.add(SeasonalEffects(code=code, description=desc))

    session.commit()

if __name__ == "__main__":
    seed_soil_quality()
    seed_soil_type()
    seed_irrigation_source()
    seed_environmental_factor()
    seed_access_to_input()
    seed_input_source()
    seed_variety()
    seed_planting_method()
    seed_planting_distance()
    seed_intercrop_crops()
    seed_pest_type()
    seed_pest_impact()
    seed_control_method()
    seed_control_frequency()
    seed_soil_testing()
    seed_testing_frequency()
    seed_soil_conservation()
    seed_conservation_techniques()
    seed_seasonal_effects()