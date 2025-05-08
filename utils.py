import pandas as pd
import numpy as np
import unicodedata
import spacy
import re
import subprocess
import sys
from wordcloud import STOPWORDS

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

def cargar_modelo_spacy():
    try:
        return spacy.load("es_core_news_sm")
    except OSError:

        # Descargar el modelo si no está instalado
        subprocess.run([sys.executable, "-m", "spacy", "download", "es_core_news_sm"], check=True)
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
    doc = nlp(texto)
    resultado = ""
    for token in doc:
        if normalizar(token.lemma_.lower()) in palabras_clave:
            resultado += f"<mark>{token.text}</mark>"
        else:
            resultado += token.text_with_ws
    return resultado

def configurar_fechas(df, columna_temporal='Marca temporal'):
    df[columna_temporal] = pd.to_datetime(df[columna_temporal], errors='coerce')
    df['Fecha'] = df[columna_temporal].dt.date
    return df

def generar_serie_temporal(df, columna_filtro, valores_filtrar, columna_agrupar='Fecha'):
    df_filtrado = df[df[columna_filtro].isin(valores_filtrar)]
    
    serie_ancha = (
        df_filtrado.groupby(columna_agrupar)[columna_filtro]
        .value_counts()
        .unstack()
        .fillna(0)
    )
    
    serie_larga = (
        serie_ancha
        .reset_index()
        .melt(id_vars=columna_agrupar, var_name='Tipo', value_name='Cantidad')
    )
    
    return serie_larga
