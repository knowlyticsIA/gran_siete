import pandas as pd
import numpy as np

def cargar_datos(url):
    return pd.read_csv(url)

def limpiar_datos(df):
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

    bins = [0, 20, 30, 40, 50, 100]
    labels = ['<20', '20-29', '30-39', '40-49', '50+']
    df['Grupo_Edad'] = pd.cut(df['Edad'], bins=bins, labels=labels)

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

    return df
