import requests

# CHAVE DE API OWM ATUALIZADA
OWM_API_KEY = "INSIRA A SUA CHAVE AQUI" 
OWM_AQ_URL = "http://api.openweathermap.org/data/2.5/air_pollution/forecast"
# NOVO ENDPOINT DE GEOCODING
OWM_GEO_URL = "http://api.openweathermap.org/geo/1.0/direct"

def get_coordinates_by_city(city_name):
    """
    Converte o nome de uma cidade em Latitude e Longitude.
    Retorna (lat, lon) ou None.
    """
    params = {
        'q': f"{city_name},BR", # Adiciona BR para focar no Brasil
        'limit': 1,
        'appid': OWM_API_KEY,
    }
    
    try:
        response = requests.get(OWM_GEO_URL, params=params, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        
        if data and len(data) > 0:
            # Retorna a lat e lon da primeira correspondência
            return str(data[0]['lat']), str(data[0]['lon']), data[0].get('name')
        
        return None, None, None # Cidade não encontrada

    except requests.exceptions.RequestException as e:
        print(f"Erro na geocodificação: {e}")
        return None, None, None


def fetch_air_quality_data(latitude, longitude):
    """
    Busca o IQA e concentrações de poluentes na OpenWeatherMap (OWM).
    """
    if not OWM_API_KEY:
        print("ERRO: A chave de API da OpenWeatherMap não está configurada.")
        return None

    params = {
        'lat': latitude,
        'lon': longitude,
        'appid': OWM_API_KEY,
    }
    
    print(f"Buscando dados OWM para Lat: {latitude}, Lon: {longitude}...")
    
    try:
        response = requests.get(OWM_AQ_URL, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if not data or not data.get('list'):
            print("Dados da OWM não encontrados para esta localização.")
            return None

        current_data = data['list'][0]
        
        return {
            'aqi_owm': current_data['main']['aqi'], 
            'components': current_data['components']
        }

    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar dados da OWM: {e}")
        return None