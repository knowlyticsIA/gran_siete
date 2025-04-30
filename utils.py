import pandas as pd
import numpy as np
import unicodedata
import spacy
import re
from datetime import datetime



# Función para cargar los datos
def cargar_datos(url):
    return pd.read_csv(url)

# Función para eliminar género (en las ocupaciones)
def eliminar_genero(texto, excepciones=None):
    if excepciones is None:
        excepciones = []

    if pd.isna(texto) or not isinstance(texto, str):
        return ""

    texto_lower = texto.lower().strip()

    if any(excepcion in texto_lower for excepcion in excepciones):
        return texto_lower

    texto_sin_genero = re.sub(r"\b(\w+)(o|a)\b", r"\1", texto_lower)
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
        df['Edad'] = datetime.now().year - df['Año_Nacimiento_Clean']
        
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
    excepciones = ["chef", "estudiante", "docente", "periodista"]
    if 'Ocupación' in df.columns:
        df['Profesión'] = (
            df['Ocupación']
            .fillna("")
            .astype(str)
            .str.lower()
            .apply(lambda texto: eliminar_genero(texto, excepciones)))
        
    return df

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
    original = palabra.lower().strip() 

    if neutralizar_genero:
        # Neutralización para palabras terminadas en 'o'/'a' con lema similar terminado en 'n'
        if original.endswith(('o', 'a')) and len(original) > 2 and lema.startswith(original[:-1]):
            base = original[:-1]
            return f"{base}[oa]"
        # Neutralización para lemas que terminan en 'o'/'a'
        elif lema.endswith(('o', 'a')) and len(lema) > 2:
            return f"{lema[:-1]}[oa]"

    return lema


def normalizar(texto):
    if pd.isna(texto) or not isinstance(texto, str):
        return ""
    return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')


def obtener_stopwords_es():
    from wordcloud import STOPWORDS
    stopwords = set(STOPWORDS)
    stopwords.update({
        "que", "de", "en", "y", "la", "el", "los", "con", "las", "un", "una", 
        "es", "se", "por", "para", "como", "me", "nos", "le", "les", "te", 
        "lo", "al", "del", "su", "sus", "este", "esta", "estos", "estas"
    })
    return stopwords

def buscar_comentarios(df, palabra_clave, columna, minimo_longitud=4):
    palabra_clave_normalizada = normalizar(palabra_clave.strip().lower())
    palabras = palabra_clave_normalizada.split()  
    
    formas_a_buscar = set()
    
    for pal in palabras:
        lema = lematizar_palabra(pal)  
        normalizado_lema = normalizar(lema)  

        if len(pal) >= minimo_longitud: 
            formas_a_buscar.add(pal[:minimo_longitud])
        if len(normalizado_lema) >= minimo_longitud:
            formas_a_buscar.add(normalizado_lema[:minimo_longitud])

    columna_normalizada = df[columna].fillna("").apply(normalizar)
    mascara = columna_normalizada.apply(
        lambda texto: any(forma in texto for forma in formas_a_buscar)
    )
    
    return df.loc[mascara], formas_a_buscar


def resaltar_palabras(texto, palabras_clave, nlp):
    """Resalta palabras clave en un texto"""
    doc = nlp(texto)
    resultado = ""
    for token in doc:
        if normalizar(token.lemma_.lower()) in palabras_clave:
            resultado += f"<mark>{token.text}</mark>"
        else:
            resultado += token.text_with_ws
    return resultado