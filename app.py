import streamlit as st
from utils import cargar_datos, limpiar_datos, cargar_modelo_spacy, lematizar_palabra
from graficos import grafico_torta, grafico_barras, graficos_cruzados, grafico_barras_conteo, generar_wordcloud

nlp = cargar_modelo_spacy()

# Configuración
st.set_page_config(layout="wide")
st.title("Dashboard de La Gran Siete")

# Cargar y limpiar datos
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSWYoXcIYju3SRMVWUEyNnLW-PurXGm4wCFiEBqOUk-chJzvdhY5y071WdIPr8IBm6VI3hhvinoLPkk/pub?output=csv"
df_raw = cargar_datos(sheet_url)
df = limpiar_datos(df_raw)

# Sidebar de navegación
st.sidebar.title("Navegación")
tabs = [
    "📌 Introducción",
    "🧑‍🤝‍🧑 Perfil del público",
    "🧢 Colaboración económica",
    "🔀 Cruces entre variables",
    "📝 Comentarios y mejoras"
]
selected_tab = st.sidebar.radio("Ir a:", tabs)

# Tab 1: Introducción
if selected_tab == "📌 Introducción":
    st.markdown("""
    Este dashboard tiene como propósito ofrecer una visión clara y estructurada de los datos que conforman el público de La Gran Siete. Aquí se presentan las percepciones y comportamientos de las personas que participan activamente en nuestros eventos, permitiéndonos entender mejor las dinámicas de la comunidad y cómo podemos seguir mejorando.
    
    ### En este espacio podrás explorar:
    - 👥 **El perfil de nuestros participantes**: Conociendo quiénes son, sus edades, y cómo se conectan con nuestro proyecto.
    - 💡 **Sus opiniones y percepciones**: Qué piensan sobre nuestras propuestas y actividades, y cómo evalúan su experiencia.
    - 🎭 **Su participación en los eventos**: Cómo viven y se sienten dentro de los eventos que organizamos.
    - 💼 **La colaboración económica**: Quiénes colaboran con la gorra y qué factores están asociados a esa decisión.
    - ❤️ **Áreas de mejora**: Identificar oportunidades para seguir creciendo juntos y hacer de La Gran Siete un proyecto aún más inclusivo y enriquecedor.
    """)

# Tab 2: Perfil del Público
elif selected_tab == "🧑‍🤝‍🧑 Perfil del público":
    st.header("¿Quién es el público de La Gran Siete?")
    torta_columnas = ['¿Cómo nos conociste?', '¿Con qué frecuencia venís a la "Tiene que Salir"?', '¿Asistís a eventos similares de otros centros culturales?']
    barras_columna = ['Profesión', '¿En qué zona vivís?', '¿Pudiste colaborar con la entrada a la gorra?', '¿Consumiste algo en la barra?', '¿Qué es lo que más te gusta de La Gran Siete?', 'Grupo_Edad']
    
    for col in df.columns:
        if col in torta_columnas:
            st.subheader(col)
            grafico_torta(df, col)
        elif col in barras_columna:
            st.subheader(col)
            if col == 'Ocupación':
                grafico_barras(df, 'Profesión', orientacion='horizontal')
            else:
                grafico_barras(df, col, orientacion='horizontal')

# Tab 3: Colaboración económica
elif selected_tab == "🧢 Colaboración económica":
    st.header("¿Dónde deja el dinero el público?")
    columnas = ['¿Pudiste colaborar con la entrada a la gorra?', '¿Consumiste algo en la barra?']
    
    for col in columnas:
        if col in df.columns:
            st.subheader(col)
            grafico_barras(df, col, orientacion='horizontal')

# Tab 4: Cruces entre variables
elif selected_tab == "🔀 Cruces entre variables":
    combinaciones_validas = {
        'Profesión': ['¿En qué zona vivís?', '¿Con qué frecuencia venís a la "Tiene que Salir"?', '¿Consumiste algo en la barra?', '¿Pudiste colaborar con la entrada a la gorra?'],
        '¿Consumiste algo en la barra?': ['¿Pudiste colaborar con la entrada a la gorra?'],
        'Grupo_Edad': ['¿Cómo nos conociste?', '¿Con qué frecuencia venís a la "Tiene que Salir"?', '¿Asistís a eventos similares de otros centros culturales?', '¿Consumiste algo en la barra?', '¿Pudiste colaborar con la entrada a la gorra?']
    }
    graficos_cruzados(df, combinaciones_validas)

# Tab 5: Comentarios y mejoras
elif selected_tab == "📝 Comentarios y mejoras":
    st.header("Comentarios y sugerencias del público")
    columna_comentarios = '¿Tenés algún aporte o sugerencia para dejarnos?'

    # Gráfico de comentarios frecuentes
    st.subheader("📊 Comentarios más frecuentes")
    top_comentarios = df[columna_comentarios].value_counts().head(15)
    df_top = top_comentarios.reset_index()
    df_top.columns = [columna_comentarios, 'Frecuencia']
    grafico_barras_conteo(df_top, columna_comentarios, 'Frecuencia')

    st.subheader("🔍 Buscar en comentarios")
    palabra_clave = st.text_input(
        "Ingresa una palabra clave para filtrar comentarios:",
        placeholder="Ej: vegano, música, atención..."
    ).strip().lower()

    if palabra_clave:
        lemma = lematizar_palabra(palabra_clave)

        # Si el lema termina en "o" y la palabra clave termina en "a" o "o"
        if lemma.endswith("o") and palabra_clave.endswith(('a', 'o')):
            # Armamos el patrón que busque ambas variantes de género
            patron = fr"\b{lemma[:-1]}[oa]\w*"
        else:
            patron = fr"\b{lemma}\w*"

        mascara = df[columna_comentarios].str.contains(
            patron,
            case=False,
            na=False,
            regex=True
        )
        comentarios_filtrados = df[mascara]

        if comentarios_filtrados.empty:
            st.warning("⚠️ No se encontraron comentarios con ese término.")
        else:
            if len(comentarios_filtrados) <= 3:
                st.success(f"📌 {len(comentarios_filtrados)} comentarios encontrados:")
                for idx, row in comentarios_filtrados.iterrows():
                    texto = str(row[columna_comentarios])
                    doc = nlp(texto)
                    resaltado = ""
                    for token in doc:
                        if token.lemma_.lower() == lemma:
                            resaltado += f"<mark>{token.text}</mark>"
                        else:
                            resaltado += token.text_with_ws
                    with st.expander(f"✏️ Comentario #{idx + 1}"):
                        st.markdown(resaltado, unsafe_allow_html=True)
            else:
                st.info(f"🔍 {len(comentarios_filtrados)} comentarios encontrados:")
                generar_wordcloud(comentarios_filtrados[columna_comentarios].dropna().tolist())