import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import streamlit as st
from wordcloud import WordCloud, STOPWORDS

def grafico_torta(df, columna):
    fig, ax = plt.subplots(figsize=(3.5, 3.5))
    df[columna].value_counts().plot.pie(autopct='%1.1f%%', startangle=90, ax=ax, wedgeprops={'edgecolor': 'black'})
    ax.set_ylabel("")
    st.pyplot(fig)

def grafico_barras(df, col, orientacion):
    if col in df.columns:
            conteo = df[col].value_counts(normalize=True).sort_values(ascending=False if orientacion == 'horizontal' else False) * 100
            fig, ax = plt.subplots(figsize=(8, 4.5))
            if orientacion == 'horizontal':
                sns.barplot(x=conteo.values, y=conteo.index, ax=ax, palette="crest")
                ax.set_xlabel("% de respuestas")
                ax.set_ylabel("")
            else:
                sns.barplot(x=conteo.index, y=conteo.values, ax=ax, palette="crest")
                ax.set_ylabel("% de respuestas")
                ax.set_xlabel("")
                ax.tick_params(axis='x', rotation=45)
            st.pyplot(fig)

def graficos_cruzados(df, combinaciones_validas, colormap="Set2"):
    st.header("📊 Gráfico cruzado dinámico")

    # Selector de columna segmentadora (explicativa)
    columna_segmento = st.selectbox("Variable explicativa", list(combinaciones_validas.keys()))

    # Selector de columna objetivo (a explicar)
    opciones_objetivo = combinaciones_validas.get(columna_segmento, [])
    columna_objetivo = st.selectbox("Variable a explicar", opciones_objetivo)

    # Botón para generar gráfico
    if st.button("Generar gráfico"):
        tabla = pd.crosstab(df[columna_objetivo], df[columna_segmento], normalize='columns') * 100
        tabla = tabla.round(1)

        if tabla.index.dtype == 'O':
            tabla = tabla.sort_index()

        # Preparar datos para graficar
        df_plot = tabla.reset_index().melt(id_vars=columna_objetivo, var_name=columna_segmento, value_name='Porcentaje')

        # Gráfico
        fig, ax = plt.subplots(figsize=(4, 4))
        sns.barplot(data=df_plot, x='Porcentaje', y=columna_objetivo, hue=columna_segmento, palette="crest", ax=ax)

        ax.set_xlabel("Porcentaje (%)")
        ax.set_ylabel("")
        ax.set_title("")
        ax.legend(title=columna_segmento, bbox_to_anchor=(1.05, 0.5), loc='center left')
        st.pyplot(fig)


def grafico_barras_conteo(df, col_categoria, col_valor):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    sns.barplot(x=col_valor, y=col_categoria, data=df, ax=ax, palette="crest")
    ax.set_xlabel("Frecuencia de menciones")
    ax.set_ylabel("")
    st.pyplot(fig)


def generar_wordcloud(textos):
    from utils import obtener_stopwords_es
    
    text_joined = " ".join(str(t) for t in textos if pd.notna(t))
    wordcloud = WordCloud(
        width=800, 
        height=400, 
        background_color='white',
        stopwords=obtener_stopwords_es(),  
        colormap='tab10'
    ).generate(text_joined)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)