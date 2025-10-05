import streamlit as st
import requests

# Ajuste a URL base se o seu Flask não estiver rodando localmente (127.0.0.1)
API_BASE_URL = "http://127.0.0.1:5000"

st.set_page_config(page_title="AeroVigil Dashboard", layout="centered")
st.title("🌍 AeroVigil - Monitoramento da Qualidade do Ar")

# --- Seção de Configuração de Busca ---
st.header("🔍 Buscar Dados por Localização")
search_type = st.radio("Método de Busca:", ('Coordenadas (Lat/Lon)', 'Nome da Cidade'), horizontal=True)

search_term = ""

if search_type == 'Coordenadas (Lat/Lon)':
    col_lat, col_lon = st.columns(2)
    lat = col_lat.text_input("Latitude", "-14.8615")
    lon = col_lon.text_input("Longitude", "-40.8442")
    if lat and lon:
        search_term = f"lat={lat}&lon={lon}"
else:
    city_name = st.text_input("Nome da Cidade (Ex: Salvador)", "Vitória da Conquista")
    if city_name:
        search_term = f"city={city_name}"

# --- Seção de Dados em Tempo Real ---

if st.button("Buscar Qualidade do Ar"):
    if not search_term:
        st.warning("Por favor, insira coordenadas ou o nome da cidade.")
    else:
        url = f"{API_BASE_URL}/api/air_quality?{search_term}"
        
        try:
            r = requests.get(url)
            
            # O Back-end retorna dados ou fallback com status 200 (OK)
            if r.status_code == 200:
                data = r.json()
                
                status = data['status']
                
                st.subheader(f"Status em: {data['location_name']}")
                
                # Trata a Lógica de Fallback (Cobertura Indisponível)
                if status == 'Cobertura Indisponível':
                    st.warning("⚠️ Cobertura Indisponível para esta área. Exibindo dados de fallback.")
                    st.metric("IQA", data['aqi'], help="Valor neutro (50) para área sem monitoramento.")
                    st.info(f"**Status:** {status} | **Sugestão:** {data['suggestion']}")
                
                # Trata dados REAIS
                else:
                    color = data['color']
                    # Mapeia cores do Back-end para emojis ou estilos do Streamlit
                    color_map = {'green': '✅', 'yellow': '🟡', 'orange': '🟠', 'red': '🔴'}
                    emoji = color_map.get(color, '⚫')
                    
                    st.metric("IQA", data['aqi'], help=f"Índice de Qualidade do Ar. Fonte: {data['source']}")
                    st.write(f"**{emoji} Status:** **{status}**")
                    st.success(f"**Sugestão de Ação:** {data['suggestion']}")
                    
                    # Para usuários avançados
                    st.caption(f"Poluente Principal (PM2.5): {data['main_pollutant'].get('pm25', 'N/A')} µg/m³")

            # Trata erros que o Flask retorna como erro HTTP (ex: 404 Cidade não encontrada)
            else:
                st.error(f"Erro {r.status_code}: Falha na busca ou {r.json().get('error', 'Erro Desconhecido')}")
        
        except requests.exceptions.ConnectionError:
            st.error("🚨 Erro de Conexão: Certifique-se de que o servidor Flask está rodando em http://127.0.0.1:5000.")


# --- Seção de Previsão ---
st.header("📈 Previsão para Amanhã")

if st.button("Gerar Previsão", key="btn_forecast"):
    r = requests.get(f"{API_BASE_URL}/api/forecast")
    
    if r.status_code == 200:
        data = r.json()
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Otimista", data['aqi_optimistic'], help="Melhor cenário possível.")
        col2.metric("Média", data['aqi_average'], help="Previsão mais provável.")
        col3.metric("Pessimista", data['aqi_pessimistic'], help="Pior cenário possível (alerta!).")
        
        st.info(data['note'])
    else:
        st.error(f"Erro {r.status_code}: {data.get('error')}")