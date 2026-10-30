import folium as fl
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium
from datos_limpios import cantidad_duplicados, cargar_datos

felinos = cargar_datos()

st.image("images/puma_blanco.png", width=500)
st.title("Mapa")


def generar_mapa():
    attr = (
        '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> '
        'contributors, &copy; <a href="https://cartodb.com/attributions">CartoDB</a>'
    )
    tiles = 'https://wms.ign.gob.ar/geoserver/gwc/service/tms/1.0.0/capabaseargenmap@EPSG%3A3857@png/{z}/{x}/{-y}.png'
    m = fl.Map(
        location=(-33.457606, -65.346857),
        control_scale=True,
        zoom_start=5,
        name="es",
        tiles=tiles,
        attr=attr,
    )
    return m


# Un color por especie
colores = {
    "Puma concolor": "red",
    "Puma yagouaroundi": "gray",
    "Panthera onca": "black",
    "Leopardus pardalis": "green",
    "Leopardus geoffroyi": "blue",
    "Leopardus guigna": "purple",
    "Leopardus tigrinus": "deeppink",
    "Leopardus wiedii": "teal",
    "Leopardus pajonales": "gold",
}

mapa = generar_mapa()


def agregar_marca(row):
    color = colores[row["species"]]
    anio = "sin fecha" if pd.isna(row["year"]) else int(row["year"])
    fl.CircleMarker(
        location=[row["lat"], row["lng"]],
        radius=6,
        color=color,
        fill=True,
        fill_color=color,
        popup=f"{row['species']} ({anio})",
    ).add_to(mapa)


anio_min = int(felinos["year"].min())
anio_max = int(felinos["year"].max())

col1, col2 = st.columns([0.3, 0.7])

with col1:
    elegidas = st.multiselect(
        "Especies a mostrar",
        sorted(colores.keys()),
        default=["Puma concolor"],
    )
    rango = st.slider(
        "Años de avistamiento",
        anio_min,
        anio_max,
        (anio_min, anio_max),
    )
    con_sin_fecha = st.checkbox("Incluir registros sin fecha", value=True)
    sin_dup = st.checkbox(
        f"Quitar registros repetidos ({cantidad_duplicados()})", value=False
    )

    # Cargamos los datos según la casilla de repetidos
    felinos = cargar_datos(sin_duplicados=sin_dup)

    # Filtro por especie y después por años
    datos = felinos[felinos["species"].isin(elegidas)]
    en_rango = datos["year"].between(rango[0], rango[1]) | (
        datos["year"].isna() & con_sin_fecha
    )
    datos = datos[en_rango]

    st.metric("Avistamientos en el mapa", len(datos))
    for esp in elegidas:
        st.markdown(
            f"<span style='color:{colores[esp]}; font-size:18px'>●</span> {esp}",
            unsafe_allow_html=True,
        )

if len(datos) > 0:
    datos.apply(agregar_marca, axis=1)

with col2:
    st_folium(mapa, key="felinos", width=700, height=550, returned_objects=[])