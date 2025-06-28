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

# --- Carga de datos ---
# Ruta al archivo CSV. Asegúrate de que coincida con la ubicación real.
CSV_FILE = "data/CLIMA_2505.csv"

@st.cache_data # Decorador para cachear los datos y evitar recargarlos en cada interacción
def load_data(file_path):
    try:
        # Asegúrate de que 'Fecha' o la columna de fecha correcta sea interpretada como fecha
        df = pd.read_csv(file_path, parse_dates=['DAY'], dayfirst=True) # Usa dayfirst=True si tus fechas son DD/MM/AAAA
        return df
    except FileNotFoundError:
        st.error(f"Error: El archivo {file_path} no se encontró. Asegúrate de que esté en la carpeta 'data/'.")
        return pd.DataFrame() # Retorna un DataFrame vacío en caso de error
    except Exception as e:
        st.error(f"Error al cargar los datos: {e}. Revisa el formato de tu CSV y los nombres de las columnas.")
        return pd.DataFrame()

df = load_data(CSV_FILE)

if not df.empty:
    st.subheader("Primeros Registros de Datos Climáticos")
    st.write(df.head()) # Muestra las primeras 5 filas del DataFrame

    st.write("---") # Una línea divisoria para separar secciones

# --- Funcionalidades futuras (resto del código ya existente) ---
st.subheader("Funcionalidades futuras:")
st.write("- Selección de mes y comparación de días por año.")
st.write("- Visualización de promedios históricos.")
st.write("- Análisis de temperaturas extremas.")

st.info("¡Estamos construyendo tu herramienta de análisis climático!")