import requests
import pandas as pd
import matplotlib.pyplot as plt

# Coordenadas aproximadas de Coccoloba Beach (La Punta de los Remedios)
LAT = 11.238
LON = -73.216

print("--- 1. CONECTANDO CON SATÉLITES METEOROLÓGICOS (Open-Meteo) ---")

# URL de la API de Open-Meteo (Datos históricos de 2024-2025)
# Pedimos: Temperatura a 2m y Velocidad del viento a 10m
url = "https://archive-api.open-meteo.com/v1/archive"
params = {
    "latitude": LAT,
    "longitude": LON,
    "start_date": "2024-01-01",
    "end_date": "2024-12-31",
    "daily": ["temperature_2m_max", "temperature_2m_min", "wind_speed_10m_max"],
    "timezone": "America/Bogota"
}

response = requests.get(url, params=params)
data = response.json()

# Procesamos los datos en un DataFrame
df_clima = pd.DataFrame({
    'Fecha': data['daily']['time'],
    'Temp_Max': data['daily']['temperature_2m_max'],
    'Temp_Min': data['daily']['temperature_2m_min'],
    'Viento_Max_kmh': data['daily']['wind_speed_10m_max']
})

# Convertir fecha a formato datetime
df_clima['Fecha'] = pd.to_datetime(df_clima['Fecha'])
df_clima['Mes'] = df_clima['Fecha'].dt.month_name()

print(f"--> Datos descargados exitosamente: {len(df_clima)} días analizados.")

# --- ANÁLISIS PARA LA JUNTA ---

print("\n--- 2. HALLAZGOS BIOCLIMÁTICOS (Argumento de Venta) ---")

# Promedio de viento por mes
viento_promedio = df_clima.groupby('Mes')['Viento_Max_kmh'].mean().sort_values(ascending=False)
print("\n VELOCIDAD DEL VIENTO PROMEDIO (¿Funciona la ventilación natural?):")
print(viento_promedio)

# Días ideales (Noches frescas < 24°C y Viento > 15 km/h)
dias_frescos = df_clima[(df_clima['Temp_Min'] < 25) & (df_clima['Viento_Max_kmh'] > 15)]
print(f"\n DÍAS DE CONFORT NATURAL AL AÑO: {len(dias_frescos)} de 366")

# Guardar para el portafolio
df_clima.to_csv("datos_climaticos_dibulla.csv", index=False)
print("\nArchivo 'datos_climaticos_dibulla.csv' generado.")