import streamlit as st
import pandas as pd
from database import session
from auth import has_permission
from utils.ui import hide_streamlit_ui, apply_global_css
from utils.sidebar import render_sidebar

from database import (
    session,
    Farmer,
    Farm,
    AbacaCultivation,
    PestManagement,
    SoilManagement,
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
    SeasonalEffects
)

# =========================
# ACCESS CONTROL
# =========================
if not has_permission("manage_references"):
    st.error("Access Denied")
    st.stop()

st.set_page_config(page_title="Reference Management", layout="wide")

hide_streamlit_ui()
render_sidebar()
apply_global_css()

st.title("Reference Data Management")

# =========================
# ALL MODELS
# =========================
REFERENCE_MODELS = {
    "Soil Quality": SoilQuality,
    "Soil Type": SoilType,
    "Irrigation Source": IrrigationSource,
    "Environmental Factor": EnvironmentalFactor,
    "Access To Inputs": AccessToInputs,
    "Input Source": InputSource,
    "Variety": Variety,
    "Planting Method": PlantingMethod,
    "Planting Distance": PlantingDistance,
    "Intercrop Crops": IntercropCrops,
    "Pest Type": PestType,
    "Pest Impact": PestImpact,
    "Control Method": ControlMethod,
    "Control Frequency": ControlFrequency,
    "Soil Testing": SoilTesting,
    "Testing Frequency": TestingFrequency,
    "Soil Conservation": SoilConservation,
    "Conservation Techniques": ConservationTechniques,
    "Seasonal Effects": SeasonalEffects,
}

# =========================
# SELECT REFERENCE TABLE
# =========================
selected_table = st.selectbox("Select Reference Type", list(REFERENCE_MODELS.keys()))
Model = REFERENCE_MODELS[selected_table]

st.divider()

# =========================
# LOAD DATA
# =========================
records = session.query(Model).all()

df = pd.DataFrame([
    {
        "No": i + 1,
        "Code": r.code,
        "Description": r.description
    }
    for i, r in enumerate(records)
])

st.subheader(f"{selected_table} Records")
st.dataframe(df, use_container_width=True, hide_index=True)

# =========================
# ADD / UPDATE FORM
# =========================
st.divider()
st.subheader(f"Add / Update {selected_table}")

record_map = {f"{r.code} - {r.description}": r for r in records}

selected_record = st.selectbox("Select Record (for update)", ["New"] + list(record_map.keys()))

code = st.text_input("Code")
description = st.text_input("Description")

if st.button("Save"):

    if not code or not description:
        st.warning("Code and Description are required")

    else:
        # UPDATE
        if selected_record != "New":
            obj = record_map[selected_record]
            obj.code = code
            obj.description = description

        # CREATE
        else:
            new_obj = Model(code=code, description=description)
            session.add(new_obj)

        session.commit()
        st.success("Saved successfully")
        st.rerun()

# =========================
# DELETE
# =========================
st.divider()
st.subheader("Delete Record")

delete_map = {f"{r.code} - {r.description}": r for r in records}

to_delete = st.selectbox("Select Record to Delete", list(delete_map.keys()))

if st.button("Delete"):
    obj = delete_map[to_delete]
    session.delete(obj)
    session.commit()

    st.success("Deleted successfully")
    st.rerun()