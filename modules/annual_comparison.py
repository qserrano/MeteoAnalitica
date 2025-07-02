import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def show_annual_comparison(df):
    st.header("📈 Comparativa Anual Detallada")
    st.write("Compara la evolución diaria/mensual de una variable para todos los años disponibles en el dataset.")

    # Asegurarse de que 'DAY' es datetime y 'Año' y 'Mes' existen
    if 'DAY' not in df.columns or not pd.api.types.is_datetime64_any_dtype(df['DAY']):
        st.error("La columna 'DAY' no está en el formato de fecha y hora correcto. Por favor, revisa la carga de datos.")
        return
    if 'Año' not in df.columns:
        df['Año'] = df['DAY'].dt.year
    if 'Mes' not in df.columns:
        df['Mes'] = df['DAY'].dt.month

    # Identificar columnas numéricas para la selección de variables
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    cols_to_exclude = ['RECORD_NUMBER', 'Mes', 'Año']
    variables_analizables = [col for col in numeric_cols if col not in cols_to_exclude]

    if not variables_analizables:
        st.warning("No se encontraron columnas numéricas aptas para el análisis.")
        return

    st.sidebar.header("Opciones de Comparativa Anual")
    selected_variable = st.sidebar.selectbox(
        "Selecciona la variable a comparar:",
        options=variables_analizables
    )

    # Opción para comparar por Mes o por Día del Año
    comparison_granularity = st.sidebar.radio(
        "Granularidad de la comparación:",
        options=["Por Mes", "Por Día del Año"],
        index=1 # Por defecto en Día del Año
    )

    st.subheader(f"Comparativa de '{selected_variable.replace('_', ' ')}' por Año ({comparison_granularity})")

    # Preparar los datos para el gráfico
    if comparison_granularity == "Por Día del Año":
        # Usamos el día del año para comparar el mismo día en diferentes años
        df['Dia_del_Año'] = df['DAY'].dt.dayofyear
        # Agrupar por Día del Año y Año, y calcular la media
        # Usamos .mean() ya que es una comparativa de la evolución
        data_to_plot = df.groupby(['Dia_del_Año', 'Año'])[selected_variable].mean().unstack(level='Año')
        x_label = 'Día del Año'
        formatter = mdates.DateFormatter('%b %d') # Para mostrar Mes y Día en el eje X
        temp_dates = [pd.to_datetime(d, format='%j').replace(year=2000) for d in data_to_plot.index] # Año de referencia para el formato
    else: # Por Mes (solo el número de mes)
        # Agrupar por Mes y Año, y calcular la media
        data_to_plot = df.groupby(['Mes', 'Año'])[selected_variable].mean().unstack(level='Año')
        x_label = 'Mes del Año'
        formatter = mdates.DateFormatter('%b') # Para mostrar el nombre del mes
        temp_dates = [pd.to_datetime(str(d), format='%m').replace(day=1, year=2000) for d in data_to_plot.index] # Año de referencia para el formato

    if data_to_plot.empty:
        st.warning(f"No hay datos suficientes para generar la comparativa de '{selected_variable}'.")
        return

    # --- Gráfico de Líneas con Múltiples Series (Años) ---
    fig, ax = plt.subplots(figsize=(12, 7))

    # Iterar sobre las columnas (que son los años) y plotear cada una
    for column in data_to_plot.columns:
        # Solo si el año tiene datos válidos
        if not data_to_plot[column].isnull().all():
            ax.plot(temp_dates if comparison_granularity == "Por Día del Año" else data_to_plot.index,
                    data_to_plot[column],
                    label=str(column),
                    marker='o' if comparison_granularity == "Por Mes" else '', # Marcar solo si es por mes
                    markersize=4 if comparison_granularity == "Por Mes" else 0)

    # Configuración de los ejes y título
    ax.set_title(f'Comparativa Anual de {selected_variable.replace("_", " ")}')
    ax.set_xlabel(x_label)
    ax.set_ylabel(f'{selected_variable.replace("_", " ")} promedio')
    ax.grid(True, linestyle='--', alpha=0.7)

    # Formato del eje X para fechas si es por Día del Año
    if comparison_granularity == "Por Día del Año":
        ax.xaxis.set_major_formatter(formatter)
        # Ajustar ticks principales para que muestren meses, o cada N días
        ax.xaxis.set_major_locator(mdates.MonthLocator(bymonthday=15)) # Ticks a mitad de mes
        ax.xaxis.set_minor_locator(mdates.DayLocator(interval=7)) # Ticks menores semanales

        # Rotar las etiquetas de fecha para que no se solapen
        fig.autofmt_xdate(rotation=45)

    else: # Por Mes
        plt.xticks(data_to_plot.index, [pd.to_datetime(str(m), format='%m').strftime('%b') for m in data_to_plot.index])


    ax.legend(title="Año", bbox_to_anchor=(1.05, 1), loc='upper left') # Leyenda fuera del gráfico
    plt.tight_layout() # Ajusta el layout para que no se solape la leyenda

    st.pyplot(fig)

    # --- Tabla de Datos Agregados ---
    st.subheader("Datos Agregados por Año y " + ("Día del Año" if comparison_granularity == "Por Día del Año" else "Mes"))
    st.dataframe(data_to_plot.fillna('N/A').reset_index()) # Muestra el DataFrame pivotado