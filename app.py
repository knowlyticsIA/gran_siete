import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Configuración
st.set_page_config(layout="wide")
st.title("Dashboard de La Gran Siete")

sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSWYoXcIYju3SRMVWUEyNnLW-PurXGm4wCFiEBqOUk-chJzvdhY5y071WdIPr8IBm6VI3hhvinoLPkk/pub?output=csv"
df = pd.read_csv(sheet_url)

# Limpiar y agrupar edades
def extraer_anio(valor):
    try:
        if pd.isna(valor):
            return np.nan
        return int(str(valor)[:4])
    except:
        return np.nan

if 'Edad' in df.columns:
    df['Año_Nacimiento_Clean'] = df['Edad'].apply(extraer_anio)
    df['Edad'] = 2025 - df['Año_Nacimiento_Clean']

bins = [0, 20, 30, 40, 50, 100]
labels = ['<20', '20-29', '30-39', '40-49', '50+']
df['Grupo_Edad'] = pd.cut(df['Edad'], bins=bins, labels=labels)

columnas_a_quitar = [
    '¿Qué mejorarías en estos eventos?',
    'Año_Nacimiento_Clean',
    'Edad',
    'Marca temporal',
    'Dirección de correo electrónico',
    'Nombre'
]
for col in columnas_a_quitar:
    if col in df.columns:
        df = df.drop(columns=col)

# Columnas con gráfico de torta
torta_columnas = [
    '¿Colaboraste con la gorra?',
    'Grupo_Edad',
    '¿Con qué frecuencia asistís a estas varietés?',
    '¿Cómo nos conociste?'
]

# Tabs
st.sidebar.title("Navegación")
tabs = ["Análisis general", "Información según edad", "Información según colaboración"]
selected_tab = st.sidebar.radio("Ir a:", tabs)

if selected_tab == "Análisis general":
    st.header("Análisis general")
    for col in df.columns:
        st.subheader(col)
        if col in torta_columnas:
            fig, ax = plt.subplots(figsize=(3.5, 3.5))
            df[col].value_counts().plot.pie(autopct='%1.1f%%', startangle=90, ax=ax)
            ax.set_ylabel("")
            st.pyplot(fig)
        else:
            fig, ax = plt.subplots(figsize=(3.5, 3.5))
            sns.countplot(data=df, y=col, order=df[col].value_counts().index, color='skyblue', ax=ax)
            ax.set_xlabel("Frecuencia")
            ax.set_ylabel(col)
            plt.tight_layout()
            st.pyplot(fig)

elif selected_tab == "Información según edad":
    st.header("Distribuciones segmentadas por grupo etario")
    columnas_disponibles = [col for col in df.columns if col != 'Grupo_Edad']
    columna_seleccionada = st.selectbox("Seleccioná una pregunta para analizar", columnas_disponibles)

    if columna_seleccionada:
        st.subheader(f"{columna_seleccionada} segmentado por grupo etario")
        tabla = pd.crosstab(df[columna_seleccionada], df['Grupo_Edad'], normalize='columns') * 100

        fig1, ax1 = plt.subplots(figsize=(3.5, 3.5))
        tabla.plot(kind='bar', stacked=True, ax=ax1, colormap='Set3')
        ax1.set_xlabel(columna_seleccionada)
        ax1.set_ylabel("Porcentaje (%)")
        ax1.set_title(f"Distribución de {columna_seleccionada} por Grupo_Edad")
        ax1.legend(title='Grupo_Edad', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig1)

elif selected_tab == "Información según colaboración":
    st.header("Distribuciones segmentadas según si colaboró con la gorra")
    columna_segmento = '¿Colaboraste con la gorra?'
    columnas_disponibles = [col for col in df.columns if col != columna_segmento]
    columna_seleccionada = st.selectbox("Seleccioná una pregunta para analizar", columnas_disponibles, key='colab')

    if columna_seleccionada:
        st.subheader(f"{columna_seleccionada} segmentado por colaboración")
        tabla = pd.crosstab(df[columna_seleccionada], df[columna_segmento], normalize='columns') * 100

        fig1, ax1 = plt.subplots(figsize=(3.5, 3.5))
        tabla.plot(kind='bar', stacked=True, ax=ax1, colormap='Pastel1')
        ax1.set_xlabel(columna_seleccionada)
        ax1.set_ylabel("Porcentaje (%)")
        ax1.set_title(f"Distribución de {columna_seleccionada} según colaboración con la gorra")
        ax1.legend(title=columna_segmento, bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig1)
