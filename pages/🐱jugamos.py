import streamlit as st
from datos_limpios import cantidad_duplicados, cargar_datos

st.set_page_config(page_title="Juego de Preguntas", page_icon="🎮")
st.title("🎮 Juego de Preguntas")

# ============================================================
# Definimos las preguntas
# ============================================================
preguntas = [
    {
        "pregunta": "🐆En que provincia aparece phantera onca ?",
        "opciones": [" Chubut", "Salta", "Misiones"],
        "correcta": 2
    },
    {
        "pregunta": "🐱¿Cual es el porcentaje de avistamiento del leopardus geoffroyi? ",
        "opciones": ["3.52","8.66", "4.08"],
        "correcta": 0
    },
    {
        "pregunta": "🐯¿ En que año fue el ultimo avistamiento ? ",
        "opciones": ["2012 ","Se siguen avistando", "2011"],
        "correcta": 0
    },
]

# ============================================================
# Una pregunta por bloque, con su propio botón de verificar
# ============================================================
for i, p in enumerate(preguntas):
    st.subheader(f"Pregunta {i + 1}")
    st.write(p["pregunta"])

    # El radio guarda la elección del estudiante
    eleccion = st.radio(
        "Elegí una opción:",
        p["opciones"],
        key=f"pregunta_{i}",
        index=None,
    )

    # Cada pregunta tiene su propio botón
    if st.button("Verificar", key=f"btn_{i}"):
        if eleccion is None:
            st.warning("⚠️ Elegí una opción antes de verificar.")
        elif eleccion == p["opciones"][p["correcta"]]:
            st.balloons()
            st.success("✅ ¡Correcto!")
        else:
            correcta = p["opciones"][p["correcta"]]
            st.error(f"❌ Incorrecto. La respuesta correcta era: **{correcta}**")

    st.divider()