import pandas as pd
import os
import re

# --- CONFIGURACIÓN ---
# 1. Tu ruta actual (la misma que funcionó antes)
ruta_carpeta = r"C:\Users\Usuario\Desktop\0007894-260129131611470"

archivo_entrada = os.path.join(ruta_carpeta, "occurrence.txt")
archivo_salida = os.path.join(ruta_carpeta, "aves_corredor_caribe.csv")

# 2. Definimos el "Clúster" de búsqueda
# Usamos una expresión regular para buscar cualquiera de estos lugares
# Agregué 'Santa Marta' porque Tayrona y Mendihuaca suelen estar registrados bajo ese municipio
patron_busqueda = r"Dibulla|Palomino|Tayrona|Buritaca|Mendihuaca|Guachaca|Santa Marta|Don Diego"

columnas_interes = [
    'scientificName', 'class', 'order', 'family', 
    'decimalLatitude', 'decimalLongitude', 'eventDate', 
    'municipality', 'locality', 'verbatimLocality'
]

print(f"--> Analizando Clúster Turístico en: {archivo_entrada}")
print(f"--> Buscando lugares: {patron_busqueda}")

total_registros = 0
primera_vez = True

try:
    for chunk in pd.read_csv(archivo_entrada, sep='\t', usecols=columnas_interes, chunksize=50000, on_bad_lines='skip', low_memory=False):
        
        # FILTRO AVANZADO:
        # 1. Que sea clase Aves
        es_ave = chunk['class'].astype(str).str.contains('Aves', case=False, na=False)
        
        # 2. Que el Municipio O la Localidad mencionen nuestros lugares clave
        # Esto captura si dicen "Municipio: Santa Marta, Localidad: Parque Tayrona"
        lugar_en_municipio = chunk['municipality'].astype(str).str.contains(patron_busqueda, case=False, regex=True, na=False)
        lugar_en_localidad = chunk['locality'].astype(str).str.contains(patron_busqueda, case=False, regex=True, na=False)
        
        # Unimos condiciones
        filtro = es_ave & (lugar_en_municipio | lugar_en_localidad)
        
        resultado = chunk[filtro]
        
        if not resultado.empty:
            total_registros += len(resultado)
            if primera_vez:
                resultado.to_csv(archivo_salida, index=False, mode='w', encoding='utf-8-sig')
                primera_vez = False
            else:
                resultado.to_csv(archivo_salida, index=False, mode='a', header=False, encoding='utf-8-sig')

    print("\n" + "="*40)
    print(f"¡POTENCIAL DE MERCADO ENCONTRADO!")
    print(f"Se extrajeron {total_registros} registros de aves en todo el corredor.")
    print(f"Nuevo archivo generado: {archivo_salida}")
    print("="*40)

except Exception as e:
    print(f"Ocurrió un error: {e}")