import pandas as pd
import numpy as np
import spacy
from functools import lru_cache
import re

# Función para cargar los datos
def cargar_datos(url):
    return pd.read_csv(url)

# Función para eliminar género en las ocupaciones
def eliminar_genero(texto):
    if pd.isna(texto) or not isinstance(texto, str):
        return ""
    texto_sin_genero = re.sub(r"(o|a)\b", "", texto.lower().strip())
    return texto_sin_genero + "x" if texto_sin_genero else ""

# Función para limpiar los datos
def limpiar_datos(df):
    def extraer_anio(valor):
        try:
            if pd.isna(valor):
                return np.nan
            return int(str(valor)[:4])
        except (ValueError, TypeError):
            return np.nan

    # Limpiar la columna 'Edad' y crear 'Grupo_Edad'
    if 'Edad' in df.columns:
        df['Año_Nacimiento_Clean'] = df['Edad'].apply(extraer_anio)
        df['Edad'] = 2025 - df['Año_Nacimiento_Clean']
        
        if not df['Edad'].empty:
            try:
                bins = [0, 20, 30, 40, 50, 100]
                labels = ['<20', '20-29', '30-39', '40-49', '50+']
                df['Grupo_Edad'] = pd.cut(
                    df['Edad'], 
                    bins=bins, 
                    labels=labels,
                    right=False
                )
            except Exception as e:
                print(f"Error al crear grupos de edad: {e}")  
                df['Grupo_Edad'] = 'No especificado'

    # Limpiar columnas innecesarias
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

    # Aplicar la eliminación de género a las ocupaciones
    if 'Ocupación' in df.columns:
        df['Profesión'] = (
            df['Ocupación']
            .fillna("")
            .astype(str)
            .str.lower()
            .apply(lambda texto: eliminar_genero(texto)))
        
    return df

@lru_cache(maxsize=None)  # Cache para cargar el modelo una sola vez
def cargar_modelo_spacy():
    try:
        return spacy.load("es_core_news_sm")
    except:
        import subprocess
        subprocess.run(["python", "-m", "spacy", "download", "es_core_news_sm"])
        return spacy.load("es_core_news_sm")

def lematizar_palabra(palabra, neutralizar_genero=True):
    nlp = cargar_modelo_spacy()
    doc = nlp(palabra.lower().strip())

    if not doc:
        return palabra

    lema = doc[0].lemma_
    original = palabra.lower().strip()  # Guardamos la forma original

    if neutralizar_genero:
        # Neutralización para palabras terminadas en 'o'/'a' con lema similar terminado en 'n'
        if original.endswith(('o', 'a')) and len(original) > 2 and lema.startswith(original[:-1]):
            base = original[:-1]
            return f"{base}[oa]"
        # Neutralización para lemas que terminan en 'o'/'a'
        elif lema.endswith(('o', 'a')) and len(lema) > 2:
            return f"{lema[:-1]}[oa]"

    return lema


# Función para buscar comentarios que contengan una palabra clave
def buscar_comentarios(df, palabra_clave):
    lemma = lematizar_palabra(palabra_clave)
    return df[df['comentarios'].str.contains(lemma, case=False, na=False)]

def obtener_stopwords_es():
    from wordcloud import STOPWORDS
    stopwords_es = set(STOPWORDS)

    # Palabras adicionales a filtrar
    stopwords_es.update({
        "que", "de", "en", "y", "la", "el", "los", "con", "las", "un", "una", 
        "es", "se", "por", "para", "como", "me", "nos", "le", "les", "te", 
        "lo", "al", "del", "su", "sus", "este", "esta", "estos", "estas"
    })

    return stopwords_es
