import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def show_historical_averages(df):
    st.header("📊 Promedios Históricos")

    # Asegurarse de que las columnas de fecha, mes y día del año existan
    # 'Mes' y 'Año' ya deberían estar creadas en df si usas load_data en app.py
    # Pero necesitamos el 'Día_del_Año' para los promedios históricos
    if 'Mes' not in df.columns:
        df['Mes'] = df['DAY'].dt.month
    if 'Año' not in df.columns:
        df['Año'] = df['DAY'].dt.year

    # Crear una columna de "Día del Año" (1 a 366) para los promedios
    df['Dia_del_Año'] = df['DAY'].dt.dayofyear

    # Identificar columnas numéricas para la selección de variables
    # Excluimos 'Mes', 'Año', 'Dia_del_Año' ya que son para filtrar/agrupar, no para graficar directamente
    columnas_numericas = df.select_dtypes(include=['number']).columns.tolist()
    for col in ['Mes', 'Año', 'Dia_del_Año']:
        if col in columnas_numericas:
            columnas_numericas.remove(col)
    # También excluimos la columna 'DAY' si por alguna razón fuera numérica
    if 'DAY' in columnas_numericas:
        columnas_numericas.remove('DAY')

    if not columnas_numericas:
        st.warning("No se encontraron columnas numéricas para calcular promedios históricos.")
        return

    st.sidebar.header("Opciones de Promedios Históricos")
    selected_variable = st.sidebar.selectbox(
        "Variable para promedios históricos:",
        options=columnas_numericas
    )

    # Calcular el promedio histórico para cada día del año
    promedios_historicos = df.groupby('Dia_del_Año')[selected_variable].mean().reset_index()
    promedios_historicos.rename(columns={selected_variable: 'Promedio_Historico'}, inplace=True)

    st.subheader(f"Promedio Histórico de {selected_variable} por Día del Año")

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(promedios_historicos['Dia_del_Año'], promedios_historicos['Promedio_Historico'], label='Promedio Histórico', color='blue')

    ax.set_title(f'Evolución del Promedio Histórico de {selected_variable}')
    ax.set_xlabel('Día del Año')
    ax.set_ylabel(selected_variable)
    ax.grid(True)
    ax.legend()

    st.pyplot(fig)

    # --- Opcional: Comparar un año específico con el promedio histórico ---
    st.subheader("Comparar un Año con el Promedio Histórico")

    # Obtener la lista de años disponibles para la comparación
    años_disponibles = sorted(df['Año'].unique())
    selected_year_comparison = st.sidebar.selectbox(
        "Selecciona un año para comparar:",
        options=['Todos los años (solo promedio)'] + años_disponibles,
        index=0 # Por defecto, selecciona el promedio sin un año específico
    )

    if selected_year_comparison != 'Todos los años (solo promedio)':
        df_year_comparison = df[df['Año'] == selected_year_comparison].copy()

        # Asegurarse de que el año seleccionado tiene datos para el día del año
        df_year_comparison = df_year_comparison[['Dia_del_Año', selected_variable]].dropna()

        if not df_year_comparison.empty:
            # Unir los datos del año específico con los promedios históricos
            merged_data = pd.merge(promedios_historicos, df_year_comparison, on='Dia_del_Año', how='left')

            fig_comp, ax_comp = plt.subplots(figsize=(12, 6))
            ax_comp.plot(merged_data['Dia_del_Año'], merged_data['Promedio_Historico'], label='Promedio Histórico', color='blue')
            ax_comp.plot(merged_data['Dia_del_Año'], merged_data[selected_variable], label=f'{selected_year_comparison}', color='red', linestyle='--')

            ax_comp.set_title(f'Comparación de {selected_variable} en {selected_year_comparison} vs. Promedio Histórico')
            ax_comp.set_xlabel('Día del Año')
            ax_comp.set_ylabel(selected_variable)
            ax_comp.grid(True)
            ax_comp.legend()

            st.pyplot(fig_comp)
        else:
            st.warning(f"No hay datos suficientes para {selected_year_comparison} para realizar la comparación.")