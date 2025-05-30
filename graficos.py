import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import streamlit as st
from wordcloud import WordCloud
import altair as alt

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
    columna_segmento = st.selectbox("Variable explicativa", list(combinaciones_validas.keys()))
    opciones_objetivo = combinaciones_validas.get(columna_segmento, [])
    columna_objetivo = st.selectbox("Variable a explicar", opciones_objetivo)

    if st.button("Generar gráfico"):
        tabla = pd.crosstab(df[columna_objetivo], df[columna_segmento], normalize='columns') * 100
        tabla = tabla.round(1)
        if tabla.index.dtype == 'O':
            tabla = tabla.sort_index()

        # Preparar datos para graficar
        df_plot = tabla.reset_index().melt(id_vars=columna_objetivo, var_name=columna_segmento, value_name='Porcentaje')
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

def generar_wordcloud(textos, stopwords):
    text_joined = " ".join(str(t) for t in textos if pd.notna(t))
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color='white',
        stopwords=stopwords,
        colormap='tab10'
    ).generate(text_joined)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)

def addFooter():
    st.markdown("""
    <style>
     .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #0A0F1C;
        color: #EAEAEA;
        text-align: center;
        padding: 1em 0;
        font-size: 0.9em;
        font-family: Helvetica, sans-serif;
        z-index: 100;
    }
    .footer a {
        color: #00C2A8;
        text-decoration: none;
        margin: 0 0.5em;
    }
    @media (max-width: 600px) {
        .footer {
            font-size: 0.8em;
            padding: 0.8em 0;
        }
    }
    </style>
    <div class="footer">
        © 2025 KnowLytics IA |         
        <a href="mailto:knowlytics.ia@gmail.com">knowlytics.ia@gmail.com</a>
    </div>
    """, unsafe_allow_html=True)

def graficos_series_temporales(series, configuraciones):
    for i, serie in enumerate(series):
        if serie is None or serie.empty:
            st.warning(f"No hay datos para el gráfico {configuraciones[i]['titulo']}")
            continue
        
        selection = alt.selection_multi(fields=['Tipo'], bind='legend')
        
        chart = alt.Chart(serie).mark_line(point={"filled": True, "size": 80}, interpolate='monotone').encode(
            x='Fecha:T',
            y='Cantidad:Q',
            color='Tipo:N',  
            tooltip=['Fecha:T', 'Tipo:N', 'Cantidad:Q'],
            opacity=alt.condition(selection, alt.value(1), alt.value(0.1))
        ).add_selection(
           selection
        ).properties(
            title=configuraciones[i]['titulo'],
            height=configuraciones[i]['altura']
        ).interactive()
        
        st.altair_chart(chart, use_container_width=True)
