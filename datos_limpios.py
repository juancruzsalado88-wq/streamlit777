import pandas as pd
import streamlit as st

# Provincias mal escritas y cómo se corrigen
CORRECCIONES = {"Neuquen": "Neuquén", "Santa cruz": "Santa Cruz"}


@st.cache_data
def cargar_datos(sin_duplicados=False):
    felinos = pd.read_csv("felinos_filtrado.csv", index_col=0)
    # Corregimos los nombres de provincia mal escritos
    felinos["stateProvince"] = felinos["stateProvince"].replace(CORRECCIONES)
    # Si se pide, sacamos las filas que son copia exacta de otra
    if sin_duplicados:
        felinos = felinos.drop_duplicates()
    return felinos


def cantidad_duplicados():
    felinos = pd.read_csv("felinos_filtrado.csv", index_col=0)
    return int(felinos.duplicated().sum())