import streamlit as st
import pandas as pd

# --- Configuración básica de la página ---
st.set_page_config(
    page_title="MeteoAnalitica",
    page_icon="☀️",
    layout="wide"
)

st.title("☀️ MeteoAnalitica: Datos Climáticos")

st.write("Bienvenido a MeteoAnalitica. Aquí podrás explorar y analizar los datos climáticos.")

# --- Carga de datos (Este es un marcador de posición) ---
# Más adelante, reemplazaremos esto para cargar tu archivo CSV
# df = pd.read_csv("data/datos_clima.csv") # Asumiendo que el CSV estará en una carpeta 'data'

st.write("---") # Una línea divisoria para separar secciones

st.subheader("Funcionalidades futuras:")
st.write("- Selección de mes y comparación de días por año.")
st.write("- Visualización de promedios históricos.")
st.write("- Análisis de temperaturas extremas.")

st.info("¡Estamos construyendo tu herramienta de análisis climático!")