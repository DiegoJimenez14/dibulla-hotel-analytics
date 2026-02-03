import pandas as pd
from pytrends.request import TrendReq
import os
import time

# --- CONFIGURACIÓN ---
# Usamos hl='es-CO' para simular un usuario en Colombia buscando en español
pytrends = TrendReq(hl='es-CO', tz=300, timeout=(10,25))

# Palabras clave estratégicas
# 1. El Destino vs. La Competencia
keywords_destino = ["Dibulla", "Palomino", "Parque Tayrona"]
# 2. El Nicho de Negocio (Para ver si coincide con la temporada alta)
keywords_nicho = ["Avistamiento de aves", "Turismo de bienestar", "Retiros de yoga"]

print("--- 1. CONECTANDO CON EL CEREBRO DE GOOGLE (TRENDS) ---")

try:
    # --- ANÁLISIS A: COMPARATIVA DE DESTINOS (12 Meses) ---
    print("--> Descargando tendencias de Destino (Dibulla vs Palomino)...")
    pytrends.build_payload(keywords_destino, cat=0, timeframe='today 12-m', geo='CO', gprop='')
    
    # Interés a lo largo del tiempo
    df_destino = pytrends.interest_over_time()
    
    if not df_destino.empty:
        # Limpieza: Borrar columna 'isPartial'
        df_destino = df_destino.drop(columns=['isPartial'])
        print(f"   Datos obtenidos: {len(df_destino)} semanas registradas.")
    
    # Esperamos un poco para no bloquear Google
    time.sleep(2)

    # --- ANÁLISIS B: MAPA DE CALOR (¿DÓNDE ESTÁN LOS CLIENTES?) ---
    print("--> Identificando ciudades de origen de los turistas...")
    df_region = pytrends.interest_by_region(resolution='REGION', inc_low_vol=True, inc_geo_code=False)
    # Filtramos solo regiones con búsquedas de Dibulla
    df_region = df_region[df_region['Dibulla'] > 0].sort_values(by='Dibulla', ascending=False)
    print(f"   Ciudades/Dptos interesados en Dibulla: {len(df_region)}")

    time.sleep(2)

    # --- ANÁLISIS C: VALIDACIÓN DE NICHO (AVES) ---
    print("--> Analizando tendencias del Nicho (Aves/Wellness)...")
    pytrends.build_payload(keywords_nicho, cat=0, timeframe='today 12-m', geo='CO', gprop='')
    df_nicho = pytrends.interest_over_time()
    if not df_nicho.empty:
        df_nicho = df_nicho.drop(columns=['isPartial'])

    # --- GUARDADO ESTRUCTURADO ---
    ruta_base = "dibulla-hotel-analytics/data/processed/trends/"
    os.makedirs(ruta_base, exist_ok=True)

    df_destino.to_csv(f"{ruta_base}tendencia_destinos.csv")
    df_region.to_csv(f"{ruta_base}origen_turistas.csv")
    df_nicho.to_csv(f"{ruta_base}tendencia_nicho.csv")

    print("\n--- RESUMEN EJECUTIVO (PRELIMINAR) ---")
    
    # Calcular el mes pico de Dibulla
    # Agrupamos por mes y sumamos el interés
    df_destino['Mes'] = df_destino.index.month_name()
    pico_dibulla = df_destino.groupby('Mes')['Dibulla'].mean().sort_values(ascending=False).head(3)
    
    print(" TOP 3 MESES DE BÚSQUEDA PARA 'DIBULLA':")
    print(pico_dibulla)
    
    print("\n TOP 5 DEPARTAMENTOS QUE BUSCAN 'DIBULLA':")
    print(df_region.head(5))

    print(f"\n Archivos guardados en: {ruta_base}")

except Exception as e:
    print(f"\n ERROR DE CONEXIÓN CON GOOGLE: {e}")
    print("NOTA: Google Trends a veces bloquea scripts. Si esto falla, te daré el Plan B manual.")