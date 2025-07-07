import streamlit as st
import folium
import pydeck as pdk

st.set_page_config(page_title="UK Car Accidents - Pydeck", layout="wide")

st.title("🚗 Mapa de Acidentes de Carro no Reino Unido (2014)")
st.markdown("Este mapa mostra a distribuição de acidentes de carro no Reino Unido usando a biblioteca Pydeck em uma visualização 3D interativa com Hexagon Layer.")

# Dados de acidentes (2014)
UK_ACCIDENTS_DATA = (
    'https://raw.githubusercontent.com/uber-common/'
    'deck.gl-data/master/examples/3d-heatmap/heatmap-data.csv'
)

# Camada do mapa
layer = pdk.Layer(
    "HexagonLayer",
    UK_ACCIDENTS_DATA,
    get_position=["lng", "lat"],
    auto_highlight=True,
    elevation_scale=50,
    pickable=True,
    elevation_range=[0, 3000],
    extruded=True,
    coverage=1,
)

# Visualização inicial
view_state = pdk.ViewState(
    longitude=-1.415,
    latitude=52.2323,
    zoom=6,
    min_zoom=5,
    max_zoom=15,
    pitch=40.5,
    bearing=-27.36,
)

# Renderiza no Streamlit
st.pydeck_chart(pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={"text": "Latitude: {lat}\nLongitude: {lng}"},
))
