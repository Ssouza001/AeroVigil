from flask import Flask, jsonify, request
# ATENÇÃO: get_coordinates_by_city deve ser importada do data_collector
from data_collector import fetch_air_quality_data, get_coordinates_by_city 
from processing import calculate_pm25_aqi, generate_suggestions
from model import generate_forecast

app = Flask(__name__)

# Endpoint 1: Dados de Qualidade do Ar na Região
@app.route('/api/air_quality', methods=['GET'])
def get_air_quality():
    """
    Busca dados de qualidade do ar por coordenadas (lat/lon) OU por nome da cidade (city).
    Este é o endpoint principal do AeroVigil.
    """
    # 1. RECEBIMENTO DE PARÂMETROS
    
    # Tenta obter as coordenadas (se vierem de GPS/Front-end)
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    
    # Tenta obter o nome da cidade (se vier de um campo de busca)
    city_name = request.args.get('city')
    
    location_source = "Modelo de Satélite"
    
    # --- 2. Lógica de Geocodificação ---
    if city_name:
        # Tenta converter o nome da cidade em coordenadas
        lat_found, lon_found, found_name = get_coordinates_by_city(city_name)
        
        if not lat_found or not lon_found:
            return jsonify({'error': f'Cidade "{city_name}" não encontrada no Brasil.'}), 404
        
        lat = lat_found
        lon = lon_found
        location_source = f"Cidade: {found_name}"
        
    elif not lat or not lon:
        # Se não houver lat/lon nem nome da cidade, retorna erro de parâmetro
        return jsonify({'error': 'Parâmetros lat/lon ou "city" são obrigatórios.'}), 400

    # --- 3. Busca de Dados e Fallback ---
    
    # Usa o lat/lon final (seja do GPS ou da Geocodificação)
    air_data = fetch_air_quality_data(lat, lon)
    
    # Lógica de FALLBACK para Cobertura Indisponível (VDC e outras áreas sem dados)
    if not air_data:
        # Retorna um JSON que o Front-end pode mostrar como um alerta neutro (cor cinza, AQI 50)
        return jsonify({
            'location_name': f'{location_source} (Sem monitoramento)',
            'aqi': 50, 
            'status': 'Cobertura Indisponível',
            'color': 'gray', 
            'suggestion': 'O monitoramento em tempo real falhou para esta área. Use a previsão como guia.',
            'main_pollutant': {'pm25': None},
            'source': 'Sem Fonte de Dados'
        })
    
    # --- 4. Processamento do IQA ---
    
    pm25_value = air_data['components'].get('pm2_5')
            
    if pm25_value is None:
        # Caso raro de ter dados, mas não ter PM2.5 (poluente principal)
        return jsonify({'error': 'Dados disponíveis, mas sem PM2.5.'}), 404

    # Calcula IQA (escala 0-500), Status e Cor
    aqi_value, status, color = calculate_pm25_aqi(pm25_value)
    
    # Gera Sugestão
    suggestion = generate_suggestions(aqi_value)
    
    # --- 5. RETORNA O RESULTADO FINAL ---
    return jsonify({
        'location_name': location_source,
        'aqi': aqi_value,
        'status': status,
        'color': color,
        'suggestion': suggestion,
        'main_pollutant': {'pm25': pm25_value},
        'source': f"OpenWeatherMap (OWM AQI: {air_data['aqi_owm']}/5)"
    })

# Endpoint 2: Previsões
@app.route('/api/forecast', methods=['GET'])
def get_forecast():
    """
    Gera e retorna as previsões de IQA (Média, Otimista e Pessimista).
    """
    
    forecast_data = generate_forecast(days_ahead=1)
    
    return jsonify({
        'day': 'Amanhã',
        'aqi_average': forecast_data['average_aqi'],
        'aqi_optimistic': forecast_data['optimistic_aqi'],
        'aqi_pessimistic': forecast_data['pessimistic_aqi'],
        'note': 'Previsão baseada em modelo simples de regressão. Necessita de dados históricos reais.'
    })


if __name__ == '__main__':
    print("Servidor Flask do AeroVigil rodando...")
    # Permite acesso externo para testes em mobile
    app.run(debug=True, host='0.0.0.0')