import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Importa las funciones de tus módulos
from modules.monthly_comparison import show_monthly_comparison
from modules.historical_averages import show_historical_averages
from modules.extreme_analysis import show_extreme_analysis

# --- Configuración básica de la página ---
st.set_page_config(
    page_title="MeteoAnalitica",
    page_icon="☀️",
    layout="wide"
)

st.title("☀️ MeteoAnalitica: Análisis de Datos Climáticos")

# --- Carga de datos (Cacheado para eficiencia) ---
CSV_FILE = "data/datos_clima.csv"

@st.cache_data
def load_data(file_path):
    try:
        df = pd.read_csv(file_path, parse_dates=['DAY'], dayfirst=True, decimal=',')
        # Asegurarse de que Mes y Año están disponibles si no los creas en el módulo
        df['Mes'] = df['DAY'].dt.month
        df['Año'] = df['DAY'].dt.year
        return df
    except FileNotFoundError:
        st.error(f"Error: El archivo {file_path} no se encontró. Asegúrate de que esté en la carpeta 'data/'.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error al cargar los datos: {e}. Revisa el formato de tu CSV y los nombres de las columnas.")
        st.info("Asegúrate de que la columna de fecha se llama 'DAY' y que el formato sea compatible (DD/MM/AAAA si usas dayfirst=True).")
        return pd.DataFrame()

df = load_data(CSV_FILE)

if df.empty:
    st.warning("No se pudieron cargar los datos o el archivo está vacío. Por favor, revisa el CSV.")
    st.stop() # Detiene la ejecución si no hay datos

# --- Barra Lateral de Navegación ---
st.sidebar.info("MeteoAnalitica: Tu herramienta para explorar el clima de La Pobla Tornesa.")
st.sidebar.markdown("---")

st.sidebar.title("Navegación")
options = ["Dashboard del Último Mes", "Comparación Mensual Detallada", "Promedios Históricos", "Análisis de Extremos Climáticos"] # ¡Añade la nueva opción!
choice = st.sidebar.radio("Ir a:", options)

# --- Contenido Principal Basado en la Selección del Menú ---

if choice == "Dashboard del Último Mes":
    st.header("📊 Dashboard del Último Mes")
    st.write("Aquí se muestran los análisis clave del mes más reciente disponible en tus datos.")

    if not df.empty:
        # Encuentra la fecha más reciente
        latest_date = df['DAY'].max()
        # Filtra los datos del último mes
        df_latest_month = df[(df['DAY'].dt.month == latest_date.month) & (df['DAY'].dt.year == latest_date.year)].copy()

        if not df_latest_month.empty:
            st.write(f"Datos del mes de **{latest_date.strftime('%B de %Y')}**:") # Muestra el nombre del mes y año
            # Ocultar columnas específicas
            columns_to_hide = ['RECORD_NUMBER', 'Mes', 'Año']
            columns_to_show = [col for col in df_latest_month.columns if col not in columns_to_hide]
            df_display = df_latest_month[columns_to_show].copy()
            if 'DAY' in df_display.columns:
                df_display['DAY'] = df_display['DAY'].dt.strftime('%d/%m/%Y') # Formato DD/MM/AAAA
            st.dataframe(df_display, hide_index=True) # Muestra todas las filas del último mes sin las columnas ocultas y sin el índice

            # --- Ejemplo de visualización para el dashboard del último mes ---
            # Puedes personalizar esto con los gráficos y métricas que quieras
            st.subheader("Temperaturas Diarias del Último Mes")
            
            # Asegúrate de que 'Temperatura_Maxima' y 'Temperatura_Minima' (o similar) existen en tu CSV
            # Adapta estos nombres a tus columnas reales
            temperatura_cols = [col for col in ['TEMP_MAX', 'TEMP_MIN', 'TEMP_MEDIA'] if col in df_latest_month.columns]

            if temperatura_cols:
                fig, ax = plt.subplots(figsize=(12, 6))
                for col in temperatura_cols:
                    ax.plot(df_latest_month['DAY'].dt.day, df_latest_month[col], label=col.replace('_', ' '))
                
                ax.set_title(f'Temperaturas Diarias en {latest_date.strftime("%B de %Y")}')
                ax.set_xlabel('Día del Mes')
                ax.set_ylabel('Temperatura (°C)') # Ajusta la unidad según tus datos
                ax.legend()
                ax.grid(True)
                st.pyplot(fig)
            else:
                st.warning("No se encontraron columnas de temperatura para mostrar en el dashboard.")

            st.subheader("Resumen Estadístico del Último Mes")
            st.write(df_latest_month.describe())

        else:
            st.warning("No se encontraron datos para el mes más reciente.")
    
elif choice == "Comparación Mensual Detallada":
    if not df.empty:
        # Llamada a la función del módulo de comparación mensual
        show_monthly_comparison(df.copy()) # Pasa una copia para evitar SettingWithCopyWarning
    else:
        st.error("No hay datos cargados para realizar la comparación mensual.")

elif choice == "Promedios Históricos":
    if not df.empty:
        # Llamada a la función del módulo de promedios históricos
        show_historical_averages(df.copy()) # Pasa una copia para evitar SettingWithCopyWarning
    else:
        st.error("No hay datos cargados para calcular promedios históricos.")
    
elif choice == "Análisis de Extremos Climáticos":
    if not df.empty:
        # Llamada a la función del módulo de análisis de extremos
        show_extreme_analysis(df.copy()) # Pasa una copia para evitar SettingWithCopyWarning
    else:
        st.error("No hay datos cargados para realizar el análisis de extremos climáticos.")
