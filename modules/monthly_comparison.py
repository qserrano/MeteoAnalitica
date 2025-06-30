# modules/monthly_comparison.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def show_monthly_comparison(df):
    st.header("📈 Comparación Mensual Detallada")

    # Asegúrate de que tu columna de fecha se llama 'DAY'
    # Estas columnas Mes y Año ya deberían estar creadas en df si usas el load_data de app.py
    # Pero es bueno asegurarse o crearlas aquí si el módulo es muy independiente
    if 'Mes' not in df.columns:
        df['Mes'] = df['DAY'].dt.month
    if 'Año' not in df.columns:
        df['Año'] = df['DAY'].dt.year

    # Crear una lista de meses para la selección
    meses_nombres = {
        1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
        5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
        9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
    }
    meses_disponibles = sorted(df['Mes'].unique())
    opciones_mes = {meses_nombres[m]: m for m in meses_disponibles}

    # Identificar columnas numéricas para la selección de variables
    columnas_numericas = df.select_dtypes(include=['number']).columns.tolist()
    if 'Mes' in columnas_numericas:
        columnas_numericas.remove('Mes')
    if 'Año' in columnas_numericas:
        columnas_numericas.remove('Año')
    if 'DAY' in columnas_numericas: # Por si 'DAY' se interpreta como numérico (raro)
        columnas_numericas.remove('DAY')


    if not columnas_numericas:
        st.warning("No se encontraron columnas numéricas para graficar. Asegúrate de que tus datos climáticos contienen valores numéricos (temperatura, precipitación, etc.).")
    else:
        # Controles en el sidebar
        st.sidebar.header("Opciones de Comparación Mensual")
        selected_month_name = st.sidebar.selectbox(
            "Selecciona un mes:",
            options=list(opciones_mes.keys()),
            index=list(opciones_mes.values()).index(6) if 6 in opciones_mes.values() else 0 # Por defecto Junio o el primer mes
        )
        selected_month = opciones_mes[selected_month_name]

        selected_variable = st.sidebar.selectbox(
            "Selecciona la variable a comparar:",
            options=columnas_numericas
        )

        st.write(f"Mostrando **{selected_variable}** para el mes de **{selected_month_name}** por día y año.")

        # Filtrar datos para el mes seleccionado
        df_filtered_month = df[df['Mes'] == selected_month].copy()
        df_filtered_month['Dia_Temporal'] = df_filtered_month['DAY'].dt.day

        if not df_filtered_month.empty:
            fig, ax = plt.subplots(figsize=(12, 6))

            for year in sorted(df_filtered_month['Año'].unique()):
                df_year = df_filtered_month[df_filtered_month['Año'] == year]
                ax.plot(df_year['Dia_Temporal'], df_year[selected_variable], label=str(year))

            ax.set_title(f'{selected_variable} diaria en {selected_month_name} por Año')
            ax.set_xlabel('Día del Mes')
            ax.set_ylabel(selected_variable)
            ax.legend(title='Año')
            ax.grid(True)
            plt.xticks(df_filtered_month['Dia_Temporal'].unique())

            st.pyplot(fig)
        else:
            st.warning(f"No hay datos disponibles para el mes de {selected_month_name}.")