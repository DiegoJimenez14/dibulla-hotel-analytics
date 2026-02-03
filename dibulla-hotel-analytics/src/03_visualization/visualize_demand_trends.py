import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

# --- CORRECCIÓN DE RUTAS INTELIGENTE ---
# 1. Obtenemos la ruta exacta donde está ESTE script (visualize_demand_trends.py)
script_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Subimos dos niveles para llegar a la raíz del proyecto (de src/03_viz -> src -> root)
project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))

# 3. Definimos las rutas a los datos usando esa raíz segura
ruta_dibulla = os.path.join(project_root, "data", "raw", "Dibulla.csv")
ruta_palomino = os.path.join(project_root, "data", "raw", "trends_palomino_proxy.csv")
ruta_salida = os.path.join(project_root, "outputs", "figures", "mapa_oportunidad_demanda.png")

print(f"--> Raíz del proyecto detectada: {project_root}")
print(f"--> Buscando datos en: {ruta_dibulla}")

# --- CONFIGURACIÓN DE ESTILO ---
plt.style.use('ggplot') 
colores = {'Dibulla': '#E63946', 'Palomino': '#1D3557'} 

print("--- GENERANDO GRÁFICA DE ESTRATEGIA COMERCIAL ---")

try:
    # 1. CARGA Y LIMPIEZA
    df_d = pd.read_csv(ruta_dibulla)
    df_p = pd.read_csv(ruta_palomino)
    
    # Asegurar formato fecha
    df_d['Time'] = pd.to_datetime(df_d['Time'])
    df_p['Time'] = pd.to_datetime(df_p['Time'])
    
    # Unir datos (Merge)
    df = pd.merge(df_d, df_p, on='Time', how='inner')
    
    # 2. CREACIÓN DEL LIENZO
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # 3. TRAZADO DE LÍNEAS
    ax.plot(df['Time'], df['Palomino'], color=colores['Palomino'], linestyle='--', linewidth=1.5, label='Demanda Palomino (Mercado)', alpha=0.7)
    ax.fill_between(df['Time'], df['Palomino'], color=colores['Palomino'], alpha=0.1)
    
    ax.plot(df['Time'], df['Dibulla'], color=colores['Dibulla'], linewidth=2.5, marker='o', markersize=4, label='Interés Dibulla (Orgánico)')

    # 4. ANOTACIONES DE INTELIGENCIA
    
    # Pico de Diciembre 
    # Validamos si existe dato en diciembre para evitar error
    datos_dic = df[df['Time'].dt.month == 12]
    if not datos_dic.empty:
        pico_dic = datos_dic['Dibulla'].max()
        fecha_dic = df[df['Dibulla'] == pico_dic]['Time'].values[0]
        ax.annotate('PICO REAL DIBULLA\n(Tarifa Máxima)', 
                    xy=(fecha_dic, pico_dic), xytext=(fecha_dic, pico_dic + 15),
                    arrowprops=dict(facecolor='black', shrink=0.05),
                    fontsize=10, fontweight='bold', ha='center')

    # Pico de Agosto
    datos_ago = df[df['Time'].dt.month == 8]
    if not datos_ago.empty:
        pico_ago_pal = datos_ago['Palomino'].max()
        fecha_ago = df[df['Palomino'] == pico_ago_pal]['Time'].values[0]
        ax.annotate('OPORTUNIDAD DE INTERCEPTACIÓN\n(Palomino Lleno -> Dibulla Opción B)', 
                    xy=(fecha_ago, pico_ago_pal), xytext=(fecha_ago, pico_ago_pal + 20),
                    arrowprops=dict(facecolor=colores['Palomino'], shrink=0.05),
                    fontsize=9, color=colores['Palomino'], ha='center')

    # 5. FORMATO FINAL
    ax.set_title('Ciclos de Demanda: Dibulla (Orgánico) vs. Competencia (Referencia)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Índice de Interés de Búsqueda (0-100)')
    ax.set_xlabel('Semana del Año')
    ax.legend(loc='upper left')
    ax.grid(True, alpha=0.3)
    
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    
    plt.tight_layout()
    
    # 6. GUARDAR
    # Asegurar que la carpeta output existe
    os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
    plt.savefig(ruta_salida, dpi=300) 
    print(f" Gráfica maestra guardada en: {ruta_salida}")
    # plt.show() # Descomentar si quieres verla en pantalla al ejecutar

except FileNotFoundError as e:
    print(f" ERROR: No se encontró el archivo. \nBuscado en: {e.filename}")
    print("Verifica que los archivos 'Dibulla.csv' y 'trends_palomino_proxy.csv' estén realmente en la carpeta data/raw.")
except Exception as e:
    print(f" Ocurrió un error inesperado: {e}")