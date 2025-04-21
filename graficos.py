import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import streamlit as st

def grafico_torta(df, columna):
    fig, ax = plt.subplots(figsize=(3.5, 3.5))
    df[columna].value_counts().plot.pie(autopct='%1.1f%%', startangle=90, ax=ax)
    ax.set_ylabel("")
    st.pyplot(fig)

def grafico_barras(df, columna):
    fig, ax = plt.subplots(figsize=(3.5, 3.5))
    sns.countplot(data=df, y=columna, order=df[columna].value_counts().index, color='skyblue', ax=ax)
    ax.set_xlabel("Frecuencia")
    ax.set_ylabel(columna,)
    plt.tight_layout()
    st.pyplot(fig)

def graficar_segmentado(df, columna_segmento, columna_objetivo, colormap):
    tabla = pd.crosstab(df[columna_objetivo], df[columna_segmento], normalize='columns') * 100
    fig, ax = plt.subplots(figsize=(3.5, 3.5))
    tabla.plot(kind='bar', stacked=True, ax=ax, colormap=colormap)
    ax.set_xlabel(columna_objetivo)
    ax.set_ylabel("Porcentaje (%)")
    ax.set_title(f"Distribución de {columna_objetivo} por {columna_segmento}")
    ax.legend(title=columna_segmento, bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig)
