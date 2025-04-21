import streamlit as st
from utils import cargar_datos, limpiar_datos
from graficos import grafico_torta, grafico_barras, graficar_segmentado

# Configuración
st.set_page_config(layout="wide")
st.title("Dashboard de La Gran Siete")

# Cargar y limpiar datos
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSWYoXcIYju3SRMVWUEyNnLW-PurXGm4wCFiEBqOUk-chJzvdhY5y071WdIPr8IBm6VI3hhvinoLPkk/pub?output=csv"
df_raw = cargar_datos(sheet_url)
df = limpiar_datos(df_raw)

# Columnas para gráfico de torta
torta_columnas = [
    '¿Colaboraste con la gorra?',
    'Grupo_Edad',
    '¿Con qué frecuencia asistís a estas varietés?',
    '¿Cómo nos conociste?'
]

# Navegación
st.sidebar.title("Navegación")
tabs = ["Análisis general", "Información según edad", "Información según colaboración"]
selected_tab = st.sidebar.radio("Ir a:", tabs)
if selected_tab == "Análisis general":
    st.header("Resumen general")
    st.markdown("""
    Acá podés ver un resumen de los datos recolectados en las varietés.  
    Esta primera pestaña te muestra información clave sobre el total de asistentes,  
    cómo se enteraron del espacio y una mirada general por edades.
    """)
    total = len(df)
    st.subheader("🧮 Total de respuestas registradas")
    st.metric(label=f"Cantidad de datos registrados: {total}", value=total)

    st.subheader("📊 Distribución por grupo etario")
    if 'Grupo_Edad' in df.columns:
        grafico_torta(df, 'Grupo_Edad')
    st.subheader("📣 ¿Cómo se enteraron del espacio?")
    if '¿Cómo nos conociste?' in df.columns:
       grafico_torta(df, '¿Cómo nos conociste?')

elif selected_tab == "Información según edad":
    st.header("Distribuciones segmentadas por grupo etario")
    st.markdown("""
    En esta pestaña se organiza la información según la distribución en grupos etareos:  
    menos de 20 años  
    20-29 años  
    30-39 años  
    40-49 años  
    50 años o más    
    """)
    columnas_disponibles = [col for col in df.columns if col != 'Grupo_Edad']
    columna_seleccionada = st.selectbox("Seleccioná una pregunta para analizar", columnas_disponibles)
    if columna_seleccionada:
        graficar_segmentado(df, 'Grupo_Edad', columna_seleccionada, 'Set3')

elif selected_tab == "Información según colaboración":
    st.header("Distribuciones segmentadas según si colaboró con la gorra")
    st.markdown("""
    En esta pestaña se organiza la información según si hubo o no colaboración a la gorra:  
    no colaboró  
    sí, en formato efectivo  
    sí, en formato electrónico (qr o transferencia)  
    """)
    columna_segmento = '¿Colaboraste con la gorra?'
    columnas_disponibles = [col for col in df.columns if col != columna_segmento]
    columna_seleccionada = st.selectbox("Seleccioná una pregunta para analizar", columnas_disponibles, key='colab')
    if columna_seleccionada:
        graficar_segmentado(df, columna_segmento, columna_seleccionada, 'Pastel1')
