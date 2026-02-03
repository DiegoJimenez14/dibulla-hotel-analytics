import requests
import pandas as pd
import os

# --- CONFIGURACIÓN ---
# Coordenadas de Coccoloba Beach
LAT = 11.238
LON = -73.216
project_path = os.getcwd() # Asume que lo corres desde la raíz del proyecto

print("--- 1. DESCARGANDO DATOS HORARIOS DE ALTA PRECISIÓN ---")

url = "https://archive-api.open-meteo.com/v1/archive"
params = {
    "latitude": LAT,
    "longitude": LON,
    "start_date": "2024-01-01",
    "end_date": "2024-12-31",
    "hourly": ["temperature_2m", "wind_speed_10m"], # Pedimos datos por hora
    "timezone": "America/Bogota"
}

response = requests.get(url, params=params)
data = response.json()

# Crear DataFrame
df_hora = pd.DataFrame({
    'Fecha_Hora': data['hourly']['time'],
    'Temp_C': data['hourly']['temperature_2m'],
    'Viento_kmh': data['hourly']['wind_speed_10m']
})

# Convertir a formato fecha real
df_hora['Fecha_Hora'] = pd.to_datetime(df_hora['Fecha_Hora'])
df_hora['Hora'] = df_hora['Fecha_Hora'].dt.hour
df_hora['Mes'] = df_hora['Fecha_Hora'].dt.month_name()

# --- 2. ANÁLISIS DEL "ALIVIO TÉRMICO" ---
# Queremos saber si cuando hace calor (Temp > 28°C), hay viento (> 15 km/h)

print("\n--- CICLO DIURNO DEL VIENTO (Promedio Anual) ---")
# Agrupamos por hora del día (0 a 23) para ver el comportamiento típico
ciclo_diario = df_hora.groupby('Hora')[['Temp_C', 'Viento_kmh']].mean()

# Filtramos las horas críticas (10 AM a 5 PM)
horas_calor = ciclo_diario.loc[10:17]
print(horas_calor)

# --- 3. EL DATO DE ORO: CORRELACIÓN CALOR-VIENTO ---
# ¿En qué porcentaje de las horas calurosas hay buena brisa?
horas_calientes = df_hora[df_hora['Temp_C'] > 29] # Cuando el huésped suda
horas_con_alivio = horas_calientes[horas_calientes['Viento_kmh'] > 12] # Cuando la brisa ayuda

if len(horas_calientes) > 0:
    porcentaje_alivio = (len(horas_con_alivio) / len(horas_calientes)) * 100
    print(f"\n Total horas de calor extremo (>29°C) en el año: {len(horas_calientes)}")
    print(f" De esas horas, el {porcentaje_alivio:.1f}% tienen brisa refrescante (>12 km/h).")
else:
    print("No hubo horas de calor extremo registradas.")

# Guardar
ruta_guardado = "dibulla-hotel-analytics/data/processed/clima_horario.csv"
# Aseguramos que la carpeta exista (por si acaso)
os.makedirs(os.path.dirname(ruta_guardado), exist_ok=True)
df_hora.to_csv(ruta_guardado, index=False)
print(f"\nArchivo detallado guardado en: {ruta_guardado}")