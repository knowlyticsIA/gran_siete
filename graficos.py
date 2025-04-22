import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import streamlit as st

def grafico_torta(df, columna):
    fig, ax = plt.subplots(figsize=(3.5, 3.5))
    df[columna].value_counts().plot.pie(autopct='%1.1f%%', startangle=90, ax=ax)
    ax.set_ylabel("")
    st.pyplot(fig)

def grafico_barras(df, col, orientacion):
    if col in df.columns:
            conteo = df[col].value_counts().sort_values(ascending=True if orientacion == 'horizontal' else False)
            fig, ax = plt.subplots(figsize=(8, 4.5))
            if orientacion == 'horizontal':
                sns.barplot(x=conteo.values, y=conteo.index, ax=ax, palette="crest")
                ax.set_xlabel("Cantidad de respuestas")
                ax.set_ylabel("")
            else:
                sns.barplot(x=conteo.index, y=conteo.values, ax=ax, palette="crest")
                ax.set_ylabel("Cantidad de respuestas")
                ax.set_xlabel("")
                ax.tick_params(axis='x', rotation=45)
            st.pyplot(fig)

def graficos_cruzados(df, columna_segmento, columna_objetivo, colormap,var_explicativa,title):
    tabla = pd.crosstab(df[columna_objetivo], df[columna_segmento], normalize='columns') * 100
    tabla = tabla.round(1)
    if tabla.index.dtype == 'O':
        tabla = tabla.sort_index()
    df_plot = tabla.reset_index().melt(id_vars=var_explicativa, var_name=title, value_name='Porcentaje')
    fig, ax = plt.subplots(figsize=(3.5, 3.5))
    sns.barplot(data=df_plot, x='Porcentaje', y=var_explicativa, hue=title, palette=colormap, ax=ax)

    ax.set_xlabel("Porcentaje (%)")
    ax.set_ylabel("")
    ax.set_title("")
    ax.legend(title=title, bbox_to_anchor=(1.05, 0.5), loc='center left')
    st.pyplot(fig)

def grafico_barras_conteo(df, col_categoria, col_valor):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    sns.barplot(x=col_valor, y=col_categoria, data=df, ax=ax, palette="crest")
    ax.set_xlabel("Frecuencia de menciones")
    ax.set_ylabel("")
    st.pyplot(fig)
