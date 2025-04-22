import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Configuración inicial
st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center; color: white;'>Dashboard de La Gran Siete</h1>", unsafe_allow_html=True)

# Carga de datos
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSWYoXcIYju3SRMVWUEyNnLW-PurXGm4wCFiEBqOUk-chJzvdhY5y071WdIPr8IBm6VI3hhvinoLPkk/pub?output=csv"
df = pd.read_csv(sheet_url)

# Procesamiento de edades
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

# Agrupación de edades
bins = [0, 20, 30, 40, 50, 100]
labels = ['<20', '20-29', '30-39', '40-49', '50+']
df['Grupo_Edad'] = pd.cut(df['Edad'], bins=bins, labels=labels)

# Limpieza de columnas innecesarias
columnas_a_quitar = [
    'Año_Nacimiento_Clean',
    'Edad',
    'Marca temporal',
    'Dirección de correo electrónico',
    'Nombre'
]
for col in columnas_a_quitar:
    if col in df.columns:
        df = df.drop(columns=col)

# Sidebar de navegación
st.sidebar.title("Navegación")
tabs = [
    "📌 Introducción",
    "🧑‍🤝‍🧑 Perfil del público",
    "🎩💰 Colaboración con la gorra",
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
- 🎩💰 **La colaboración económica**: Quiénes colaboran con la gorra y qué factores están asociados a esa decisión.
- ❤️ **Áreas de mejora**: Identificar oportunidades para seguir creciendo juntos y hacer de La Gran Siete un proyecto aún más inclusivo y enriquecedor.

""")

# Tab 2: Perfil del público
elif selected_tab == "🧑‍🤝‍🧑 Perfil del público":
    st.header("¿Quién es el público de La Gran Siete?")

    variables_perfil = {
        'Grupo_Edad': 'horizontal',
        '¿Cuál es tu ocupación?': 'horizontal',
        '¿En qué zona vivís?': 'horizontal',
        '¿Cómo nos conociste?': 'vertical',
        '¿Con qué frecuencia asistís a estas varietés?': 'vertical',
        '¿Asistís a eventos similares de otros centros culturales?': 'vertical',  # puede tener solo sí/no
        '¿Qué es lo que más te gusta de La Gran Siete?': 'horizontal'
    }

    for col, orientacion in variables_perfil.items():
        if col in df.columns:
            st.subheader(col)
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


# Tab 3: Colaboración con la gorra
elif selected_tab == "🎩💰 Colaboración con la gorra":
    st.header("¿Quiénes colaboran con la gorra y por qué?")

    columna_objetivo = '¿Colaboraste con la gorra?'

    def mostrar_cruce(var_explicativa, titulo):
        if columna_objetivo in df.columns and var_explicativa in df.columns:
            st.subheader(titulo)
            try:
                # Cruzamos variables y calculamos porcentajes por columna
                tabla = pd.crosstab(df[var_explicativa], df[columna_objetivo], normalize='columns') * 100
                tabla = tabla.round(1)

                # Reordenamos el índice (si es categórico con strings) para que no se vea desordenado
                if tabla.index.dtype == 'O':
                    tabla = tabla.sort_index()

                # Preparamos el DataFrame para Seaborn
                df_plot = tabla.reset_index().melt(id_vars=var_explicativa, var_name='Colaboración', value_name='Porcentaje')

                fig, ax = plt.subplots(figsize=(8, 4.5))
                sns.barplot(data=df_plot, x='Porcentaje', y=var_explicativa, hue='Colaboración', palette='pastel', ax=ax)

                ax.set_xlabel("Porcentaje (%)")
                ax.set_ylabel("")
                ax.set_title("")
                ax.legend(title="Colaboración", loc='upper right')
                st.pyplot(fig)
            except Exception as e:
                st.warning(f"No se pudo generar el gráfico para: {var_explicativa} ({e})")

    # -------------------------------
    st.markdown("### 👤 Perfil de quienes colaboran")
    mostrar_cruce('Grupo_Edad', "Colaboración con la gorra según grupo de edad")
    mostrar_cruce('¿En qué zona vivís?', "Colaboración con la gorra según zona de residencia")
    mostrar_cruce('¿Con qué frecuencia asistís a estas varietés?', "Colaboración con la gorra según frecuencia de asistencia")



# Tab 4: Cruces entre variables
elif selected_tab == "🔀 Cruces entre variables":
    st.header("Cruces entre variables")
    columnas_disponibles = df.columns.tolist()
    col1 = st.selectbox("Seleccioná la primera variable (eje X)", columnas_disponibles, key='col1')
    col2 = st.selectbox("Seleccioná la segunda variable (eje de color)", columnas_disponibles, key='col2')

    if col1 and col2 and col1 != col2:
        st.subheader(f"{col1} vs {col2}")
        
        # Calculando la tabla de contingencia con porcentaje por columna
        tabla = pd.crosstab(df[col1], df[col2], normalize='columns') * 100
        tabla = tabla.round(1)  # Redondeamos a 1 decimal

        # Reordenamos las categorías para evitar desorden visual
        if tabla.index.dtype == 'O':
            tabla = tabla.sort_index()

        # Preparamos el DataFrame para Seaborn
        df_plot = tabla.reset_index().melt(id_vars=col1, var_name=col2, value_name='Porcentaje')

        # Configuración del gráfico
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(data=df_plot, x='Porcentaje', y=col1, hue=col2, palette='Set2', ax=ax)

        ax.set_xlabel("Porcentaje (%)")
        ax.set_ylabel("")
        ax.set_title(f"Cruce entre {col1} y {col2}", fontsize=16)
        ax.legend(title=col2, loc='upper right')
        
        # Mejorar la visualización
        ax.grid(True, axis='x', linestyle='--', alpha=0.7)
        plt.xticks(rotation=45, ha='right')
        
        st.pyplot(fig)


# Tab 5: Comentarios y mejoras
elif selected_tab == "📝 Comentarios y mejoras":
    st.header("Comentarios y sugerencias del público")
    
    columna_comentarios = '¿Qué mejorarías en estos eventos?'
    
    if columna_comentarios in df.columns:
        comentarios = df[columna_comentarios].dropna()
        
        # Obtener los 15 comentarios más frecuentes
        top_comentarios = comentarios.value_counts().head(15)
        
        # Visualizar los comentarios con la frecuencia de menciones
        st.subheader("Comentarios más frecuentes")
        
        # Crear una lista de barras horizontales para los comentarios más frecuentes
        fig, ax = plt.subplots(figsize=(8, 6))
        top_comentarios.plot(kind='barh', ax=ax, color='skyblue', edgecolor='gray')
        ax.set_xlabel("Frecuencia de menciones")
        ax.set_ylabel("Comentarios")
        ax.set_title("Frecuencia de comentarios por sugerencia")
        ax.grid(True, axis='x', linestyle='--', alpha=0.7)
        plt.xticks(rotation=0)
        st.pyplot(fig)
