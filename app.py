import streamlit as st
from utils import cargar_datos, limpiar_datos
from graficos import grafico_torta, grafico_barras, graficos_cruzados, grafico_barras_conteo

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
    "Colaboración económica",
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
    - **La colaboración económica**: Quiénes colaboran con la gorra y qué factores están asociados a esa decisión.
    - ❤️ **Áreas de mejora**: Identificar oportunidades para seguir creciendo juntos y hacer de La Gran Siete un proyecto aún más inclusivo y enriquecedor.
""")

# Tab 2: Perfil del público
elif selected_tab == "🧑‍🤝‍🧑 Perfil del público":
    st.header("¿Quién es el público de La Gran Siete?")
    torta_columnas = ['Grupo_Edad', '¿Cómo nos conociste?','¿Con qué frecuencia asistís a estas varietés?','¿Asistís a eventos similares de otros centros culturales?']
    for col in df.columns:
        st.subheader(col)
        if col in torta_columnas:
            grafico_torta(df, col)
        else:
            grafico_barras(df, col, orientacion='horizontal')
    
# Tab 3: Colaboración económica
elif selected_tab == "Colaboración económica":
    st.header("¿Quiénes colaboran con la gorra y por qué?")
    columna_objetivo = '¿Colaboraste con la gorra?'
    st.markdown("### 👤 Perfil de quienes colaboran")
    # Asegurate de que cada columna esté presente antes de graficar
    posibles_columnas = [
        ('Grupo_Edad', "Colaboración con la gorra según grupo de edad"),
        ('¿En qué zona vivís?', "Colaboración con la gorra según zona de residencia"),
        ('¿Con qué frecuencia asistís a estas varietés?', "Colaboración con la gorra según frecuencia de asistencia")
    ]

    for col, titulo in posibles_columnas:
        if columna_objetivo in df.columns and col in df.columns:
            st.subheader(titulo)
            try:
                graficos_cruzados(df, columna_objetivo=col, columna_segmento=columna_objetivo, var_explicativa=col, colormap="pastel",title='Colaboración')
            except Exception as e:
                st.warning(f"No se pudo generar el gráfico para: {col} ({e})")

# Tab 4: Cruces entre variables
elif selected_tab == "🔀 Cruces entre variables":
    st.header("Cruces entre variables")
    columnas_disponibles = df.columns.tolist()
    col1 = st.selectbox("Seleccioná la primera variable (eje X)", columnas_disponibles, key='col1')
    col2 = st.selectbox("Seleccioná la segunda variable (eje de color)", columnas_disponibles, key='col2')
    if col1 and col2 and col1 != col2:
        st.subheader(f"{col1} vs {col2}")
        graficos_cruzados(df, col2, col1, 'Set2', col1, col2)

# Tab 5: Comentarios y mejoras
elif selected_tab == "📝 Comentarios y mejoras":
    st.header("Comentarios y sugerencias del público")    
    columna_comentarios = '¿Qué mejorarías en estos eventos?'
    comentarios = df[columna_comentarios].dropna()
    top_comentarios = comentarios.value_counts().head(15)
    st.subheader("Comentarios más frecuentes")
    df_top = top_comentarios.reset_index()
    df_top.columns = [columna_comentarios, 'Frecuencia']
    grafico_barras_conteo(df_top, columna_comentarios, 'Frecuencia')