import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

# Dados históricos SIMULADOS de IQA (últimos 7 dias) para treinar o modelo
HISTORICAL_AQI = np.array([55, 60, 65, 70, 75, 80, 85])
HISTORICAL_DAYS = np.arange(1, len(HISTORICAL_AQI) + 1).reshape(-1, 1)

def train_aqi_model():
    """Treina um modelo simples de Regressão Linear."""
    model = LinearRegression()
    model.fit(HISTORICAL_DAYS, HISTORICAL_AQI)
    return model

def generate_forecast(days_ahead=1):
    """
    Gera a previsão do IQA para X dias à frente e retorna cenários Otimista/Pessimista.
    (MVP: Usa margem fixa)
    """
    if len(HISTORICAL_AQI) < 2:
        # Retorna valores mockados se não houver dados históricos suficientes
        return {'average_aqi': 70, 'optimistic_aqi': 50, 'pessimistic_aqi': 90}

    model = train_aqi_model()
    
    # Prevemos o próximo dia
    day_to_predict = np.array([[len(HISTORICAL_AQI) + days_ahead]])
    
    # PREVISÃO MÉDIA
    mean_prediction = model.predict(day_to_predict)[0]
    
    # CENÁRIOS OTIMISTA E PESSIMISTA (Margem de 15%)
    margin = 0.15 * mean_prediction 
    
    optimistic_prediction = max(0, mean_prediction - margin)
    pessimistic_prediction = mean_prediction + margin
    
    return {
        'average_aqi': round(mean_prediction),
        'optimistic_aqi': round(optimistic_prediction),
        'pessimistic_aqi': round(pessimistic_prediction)
    }