import math

# Lógica de Breakpoints PM2.5 (µg/m³) e IQA (Baseado na EPA, simplificado)
PM25_BREAKPOINTS = [
    (0.0, 12.0, 0, 50, "Bom", "green"),
    (12.1, 35.4, 51, 100, "Moderado", "yellow"),
    (35.5, 55.4, 101, 150, "Insalubre para Grupos de Risco", "orange"),
    (55.5, 150.4, 151, 200, "Insalubre", "red"),
    (150.5, 250.4, 201, 300, "Muito Insalubre", "purple"),
    (250.5, 500.4, 301, 500, "Perigoso", "maroon")
]

def interpolate_aqi(c_low, c_high, i_low, i_high, c):
    """Realiza a interpolação linear para calcular o IQA."""
    # Fórmula: ((I_high - I_low) / (C_high - C_low)) * (C - C_low) + I_low
    if c_high == c_low:
        return i_low
    return round(((i_high - i_low) / (c_high - c_low)) * (c - c_low) + i_low)

def calculate_pm25_aqi(concentration):
    """Calcula o IQA (0-500) com base na concentração de PM2.5."""
    
    # Se a concentração for maior que o último breakpoint
    if concentration > 500.4:
        return 500, "Perigoso", "maroon"
        
    for c_low, c_high, i_low, i_high, status, color in PM25_BREAKPOINTS:
        # Usa uma pequena margem para lidar com problemas de float
        if c_low <= concentration <= c_high + 0.001: 
            aqi = interpolate_aqi(c_low, c_high, i_low, i_high, concentration)
            return aqi, status, color
            
    return 0, "Dados Inválidos", "gray"

def generate_suggestions(aqi_value):
    """Gera sugestões de ação com base no valor do IQA."""
    if aqi_value >= 151: 
        return "Evite exercícios ao ar livre. Pessoas com doenças respiratórias devem permanecer em ambientes fechados. Considere o uso de máscara PFF2."
    elif aqi_value >= 101: 
        return "Grupos sensíveis (crianças, idosos, asmáticos) devem limitar atividades externas. Demais podem seguir normalmente."
    elif aqi_value >= 51: 
        return "A qualidade do ar é aceitável, mas monitore se você tem sensibilidade incomum a poluentes."
    else: 
        return "Qualidade do ar excelente. Aproveite o ar livre!"