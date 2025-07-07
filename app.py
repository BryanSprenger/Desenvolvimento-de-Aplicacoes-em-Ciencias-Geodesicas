import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# Configuração da página
st.set_page_config(page_title="UK Car Accidents - Folium", layout="wide")

st.title("🚗 Mapa de Acidentes de Carro no Reino Unido (2014)")
st.markdown("Este mapa mostra a distribuição de acidentes de carro no Reino Unido usando a biblioteca **Folium**, com marcadores para cada ocorrência.")

# Carrega os dados
DATA_URL = (
    'https://raw.githubusercontent.com/uber-common/'
    'deck.gl-data/master/examples/3d-heatmap/heatmap-data.csv'
)

df = pd.read_csv(DATA_URL)

# Verifica as colunas necessárias
if "lat" not in df.columns or "lng" not in df.columns:
    st.error("Colunas 'lat' e 'lng' não encontradas nos dados.")
    st.stop()

# Cria o mapa centrado no meio do dataset
mapa = folium.Map(
    location=[df["lat"].mean(), df["lng"].mean()],
    zoom_start=6,
    tiles="CartoDB positron"
)

# Adiciona pontos ao mapa
for _, row in df.iterrows():
    folium.CircleMarker(
        location=[row["lat"], row["lng"]],
        radius=3,
        color="red",
        fill=True,
        fill_opacity=0.7,
        popup=f"Lat: {row['lat']:.4f}, Lon: {row['lng']:.4f}"
    ).add_to(mapa)

# Exibe o mapa no Streamlit
folium_static(mapa)
