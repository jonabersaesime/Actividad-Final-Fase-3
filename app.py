"""
Interfaz sencilla para demostrar la detección de Data Drift.

Permite seleccionar una variable del dataset, modificar sus valores
mediante un porcentaje y ejecutar el detector de drift.
"""

import pandas as pd
import streamlit as st

from src.drift import DriftDetector


st.set_page_config(
    page_title="Monitor de Data Drift",
    page_icon="📊",
    layout="centered",
)

st.title("Monitor de Data Drift")
st.write(
    "Selecciona una variable y modifica sus valores para comprobar "
    "si el sistema detecta un cambio en la distribución."
)

# Cargar dataset de referencia
reference_data = pd.read_csv("data/breast_cancer.csv")

# Excluir columnas que no utiliza el modelo
excluded_columns = ["id", "diagnosis", "Unnamed: 32"]

feature_columns = [
    column
    for column in reference_data.columns
    if column not in excluded_columns
]

selected_variable = st.selectbox(
    "Variable que deseas modificar",
    feature_columns,
)

change_percentage = st.slider(
    "Porcentaje de modificación",
    min_value=-100,
    max_value=300,
    value=0,
    step=1,
)

st.write(
    f"Los valores de **{selected_variable}** se modificarán en "
    f"**{change_percentage}%**."
)

if st.button("Evaluar Data Drift"):
    current_data = reference_data.copy()

    current_data[selected_variable] = (
        current_data[selected_variable]
        * (1 + change_percentage / 100)
    )

    drift_detector = DriftDetector()

    drift_result = drift_detector.detect_drift(
        reference_data[feature_columns],
        current_data[feature_columns],
    )

    st.subheader("Resultado")

    if drift_result["drift_detected"]:
        st.error("Se detectó Data Drift.")
    else:
        st.success("No se detectó Data Drift.")

    st.write(f"**Estado:** {drift_result['status']}")
    st.write(
        f"**Variables evaluadas:** "
        f"{drift_result['variables_evaluadas']}"
    )