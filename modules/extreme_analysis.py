import streamlit as st
import pandas as pd

def show_extreme_analysis(df):
    st.header("🌡️ Análisis de Extremos Climáticos")
    st.write("Identifica los días con los valores más altos o más bajos para una variable específica.")

    # Identificar columnas numéricas para la selección de variables
    # Excluimos 'Mes', 'Año' y 'Dia_del_Año' (si existe de historical_averages)
    columnas_numericas = df.select_dtypes(include=['number']).columns.tolist()
    for col in ['Mes', 'Año', 'Dia_del_Año']:
        if col in columnas_numericas:
            columnas_numericas.remove(col)
    if 'DAY' in columnas_numericas: # Por si 'DAY' se interpreta como numérico (raro)
        columnas_numericas.remove('DAY')

    if not columnas_numericas:
        st.warning("No se encontraron columnas numéricas para realizar el análisis de extremos.")
        return

    st.sidebar.header("Opciones de Extremos")
    selected_variable = st.sidebar.selectbox(
        "Selecciona la variable:",
        options=columnas_numericas
    )

    extreme_type = st.sidebar.radio(
        "Tipo de Extremo:",
        options=["Más Alta", "Más Baja"]
    )

    num_records = st.sidebar.slider(
        "Número de días a mostrar:",
        min_value=5, max_value=50, value=10, step=5
    )

    st.subheader(f"Los {num_records} días con la {selected_variable} {extreme_type}")

    # Ordenar el DataFrame según la selección
    if extreme_type == "Más Alta":
        # Asegúrate de que los valores NaN no afecten el orden
        df_sorted = df.sort_values(by=selected_variable, ascending=False, na_position='last')
    else: # Más Baja
        df_sorted = df.sort_values(by=selected_variable, ascending=True, na_position='first')

    # Seleccionar las columnas relevantes para mostrar
    # Asegúrate de incluir 'DAY' y la variable seleccionada
    columns_to_display = ['DAY', selected_variable]

    # Opcional: añadir otras columnas descriptivas si existen
    # if 'Temperatura_Maxima' in df.columns: columns_to_display.append('Temperatura_Maxima')
    # if 'Temperatura_Minima' in df.columns: columns_to_display.append('Temperatura_Minima')
    # if 'Precipitacion' in df.columns: columns_to_display.append('Precipitacion')
    # ... y así con otras columnas importantes para el contexto

    # Formatear la columna DAY para mostrar solo la fecha en formato DD/MM/AAAA
    df_sorted['DAY'] = df_sorted['DAY'].dt.strftime('%d/%m/%Y')
    
    # Mostrar solo las columnas deseadas y los 'num_records' primeros
    # Usamos .reset_index(drop=True) para limpiar el índice después de la ordenación
    df_to_show = df_sorted[columns_to_display].head(num_records).reset_index(drop=True)
    
    # Crear una tabla HTML personalizada
    table_html = """
    <div style="display: flex; justify-content: center;">
        <table style="border-collapse: collapse; width: 100%; max-width: 800px; margin: 20px auto;">
            <thead>
                <tr style="background-color: #f0f0f0; color: #333;">
    """
    
    # Agregar las cabeceras de la tabla
    for col in df_to_show.columns:
        table_html += f"<th style='text-align: center; padding: 8px; border: 1px solid #ddd;'>{col}</th>"
    
    table_html += "</tr></thead><tbody>"
    
    # Agregar las filas de datos
    for _, row in df_to_show.iterrows():
        table_html += "<tr>"
        for value in row:
            table_html += f"<td style='text-align: center; padding: 8px; border: 1px solid #ddd;'>{value}</td>"
        table_html += "</tr>"
    
    table_html += "</tbody></table></div>"
    
    # Mostrar la tabla HTML con st.markdown
    st.markdown(table_html, unsafe_allow_html=True)

    # Opcional: mostrar un pequeño gráfico de dispersión de estos puntos
    # import altair as alt # Si quieres gráficos interactivos, necesitarías instalar altair
    # chart_df = df_sorted.head(num_records).copy()
    # if not chart_df.empty:
    #     chart = alt.Chart(chart_df).mark_point().encode(
    #         x='DAY',
    #         y=selected_variable,
    #         tooltip=['DAY', selected_variable]
    #     ).properties(
    #         title=f'Top {num_records} {selected_variable} {extreme_type}'
    #     )
    #     st.altair_chart(chart, use_container_width=True)