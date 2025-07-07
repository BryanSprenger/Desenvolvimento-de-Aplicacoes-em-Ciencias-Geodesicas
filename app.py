import streamlit as st
import pandas as pd
import folium
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from streamlit_folium import folium_static

# Configuração da página
st.set_page_config(page_title="Ocorrências Geocodificadas", layout="wide")
st.title("📍 Mapeamento de Ocorrências por Logradouro")
st.markdown("Geocodificação de endereços a partir da base de dados pública.")

# URL do CSV
url = 'https://raw.githubusercontent.com/BryanSprenger/Desenvolvimento-de-Aplicacoes-em-Ciencias-Geodesicas/refs/heads/main/Dados%20ocorrencias.csv'

# Carrega os dados
df = pd.read_csv(url, sep=';', encoding='utf-8')
st.write("Visualização da base de dados original:")
st.dataframe(df.head())

# Seleciona apenas os dados com logradouro válido
df = df[df['LOGRADOURO_NOME_CURITIBA'].notnull() & (df['LOGRADOURO_NOME_CURITIBA'] != '')]

# Adiciona cidade (melhora a geocodificação)
cidade_base = "Curitiba, PR, Brasil"
enderecos = df['LOGRADOURO_NOME_CURITIBA'].astype(str) + ", " + cidade_base

# Geocodificador com controle de taxa
geolocator = Nominatim(user_agent="app_geo_ocorrencias")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

st.info("Geocodificando os endereços... pode demorar dependendo da quantidade de registros.")
coordenadas = enderecos.apply(geocode)

# Extrai lat/lon
df['location'] = coordenadas
df['lat'] = df['location'].apply(lambda loc: loc.latitude if loc else None)
df['lon'] = df['location'].apply(lambda loc: loc.longitude if loc else None)

# Filtra apenas os geocodificados com sucesso
df_marcados = df.dropna(subset=['lat', 'lon'])

# Cria o mapa com folium
mapa = folium.Map(location=[-25.43, -49.27], zoom_start=12, tiles='CartoDB positron')

for _, row in df_marcados.iterrows():
    folium.Marker(
        location=[row['lat'], row['lon']],
        popup=f"{row['LOGRADOURO']}",
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(mapa)

st.success(f"{len(df_marcados)} endereços geocodificados com sucesso.")
folium_static(mapa)

