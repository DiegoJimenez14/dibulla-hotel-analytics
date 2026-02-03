import pandas as pd
import matplotlib.pyplot as plt
import requests
import os

# --- CONFIGURACIÓN ---
# Intentamos leer el archivo local que generaste antes. Si no existe, lo descargamos.
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
ruta_datos = os.path.join(project_root, "data", "processed", "clima_horario.csv")

print("--- GENERANDO GRÁFICA DE CONFORT BIOCLIMÁTICO ---")

# 1. CARGA DE DATOS (Inteligente)
if os.path.exists(ruta_datos):
    print(f"--> Leyendo datos locales de: {ruta_datos}")
    df = pd.read_csv(ruta_datos)
else:
    print("--> No encontré el archivo local. Descargando datos de nuevo...")
    # (Fallback: Descarga rápida si borraste el archivo anterior)
    LAT, LON = 11.238, -73.216
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": LAT, "longitude": LON,
        "start_date": "2024-01-01", "end_date": "2024-12-31",
        "hourly": ["temperature_2m", "wind_speed_10m"],
        "timezone": "America/Bogota"
    }
    r = requests.get(url, params=params).json()
    df = pd.DataFrame({
        'Fecha_Hora': r['hourly']['time'],
        'Temp_C': r['hourly']['temperature_2m'],
        'Viento_kmh': r['hourly']['wind_speed_10m']
    })

# Procesar fechas
df['Fecha_Hora'] = pd.to_datetime(df['Fecha_Hora'])
df['Hora'] = df['Fecha_Hora'].dt.hour

# 2. AGRUPAR POR HORA (El Ciclo Diario Promedio)
ciclo = df.groupby('Hora')[['Temp_C', 'Viento_kmh']].mean()

# 3. VISUALIZACIÓN PROFESIONAL
fig, ax1 = plt.subplots(figsize=(12, 6))

# Eje 1: Temperatura (Rojo - Calor)
color_temp = '#D62828' # Rojo Fuego
ax1.set_xlabel('Hora del Día (00:00 - 23:00)', fontsize=12)
ax1.set_ylabel('Temperatura (°C)', color=color_temp, fontsize=12, fontweight='bold')
ax1.plot(ciclo.index, ciclo['Temp_C'], color=color_temp, linewidth=3, label='Calor (Temp)')
ax1.tick_params(axis='y', labelcolor=color_temp)
ax1.grid(True, alpha=0.3)

# Eje 2: Viento (Azul - Frescura)
ax2 = ax1.twinx()  # Instanciamos un segundo eje que comparte el eje X
color_viento = '#0077B6' # Azul Mar Caribe
ax2.set_ylabel('Velocidad Viento (km/h)', color=color_viento, fontsize=12, fontweight='bold')
# Usamos un gráfico de área para mostrar la "masa" de aire fresco
ax2.fill_between(ciclo.index, ciclo['Viento_kmh'], color=color_viento, alpha=0.2, label='Brisa Marina')
ax2.plot(ciclo.index, ciclo['Viento_kmh'], color=color_viento, linestyle='--', linewidth=2)
ax2.tick_params(axis='y', labelcolor=color_viento)

# 4. DESTAQUES ESTRATÉGICOS (Storytelling)
# Marcamos la hora crítica (12PM - 3PM) donde el Viento ayuda al Calor
plt.axvspan(11, 15, color='green', alpha=0.1, label='Zona de Confort Natural')
plt.text(13, ciclo['Viento_kmh'].max() + 1, "EFECTO 'AIRE ACONDICIONADO'\nNATURAL", 
         color='green', fontsize=10, fontweight='bold', ha='center')

# Título y Diseño
plt.title('Validación de Arquitectura Bioclimática: Ciclo Diario Promedio', fontsize=14, fontweight='bold')
fig.tight_layout()

# 5. GUARDAR
ruta_salida = os.path.join(project_root, "outputs", "figures", "grafica_confort_bioclimatico.png")
os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
plt.savefig(ruta_salida, dpi=300)
print(f" Gráfica de Clima guardada en: {ruta_salida}")
plt.show()