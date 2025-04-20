import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Configuración
st.set_page_config(layout="wide")
st.title("Dashboard de La Gran Siete")

df = pd.read_csv("datos.csv")
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

# Mostrar columnas disponibles
columnas_disponibles = [col for col in df.columns if col != 'Grupo_Edad']
columna_seleccionada = st.selectbox("Seleccioná una pregunta para analizar", columnas_disponibles)

# Gráfico 1: Distribución por grupo etario
if columna_seleccionada:
    st.subheader(f"{columna_seleccionada} segmentado por grupo etario")
    tabla = pd.crosstab(df[columna_seleccionada], df['Grupo_Edad'], normalize='columns') * 100

    fig1, ax1 = plt.subplots(figsize=(7, 4))
    tabla.plot(kind='bar', stacked=True, ax=ax1, colormap='Set3')
    ax1.set_xlabel(columna_seleccionada)
    ax1.set_ylabel("Porcentaje (%)")
    ax1.set_title(f"Distribución de {columna_seleccionada} por Grupo_Edad")
    ax1.legend(title='Grupo_Edad', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig1)

# Gráfico 2: Frecuencia general
st.subheader(f"Distribución general de {columna_seleccionada}")
fig2, ax2 = plt.subplots(figsize=(7, 4))
sns.countplot(data=df, y=columna_seleccionada, order=df[columna_seleccionada].value_counts().index, color='skyblue', ax=ax2)
ax2.set_xlabel("Frecuencia")
ax2.set_ylabel(columna_seleccionada)
plt.grid(axis='x')
plt.tight_layout()
st.pyplot(fig2)
