#  Hotel Coccoloba: Eco-Tourism Business Intelligence Suite

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-150458?style=flat&logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-11557c?style=flat&logo=matplotlib&logoColor=white)
![Open-Meteo](https://img.shields.io/badge/API-Open--Meteo-orange)
![Status](https://img.shields.io/badge/Status-Production_Ready-success)

> **Business Intelligence Strategy aplicada a la reactivación de un Hotel Ecológico en el Caribe Colombiano.** > Este proyecto transforma datos dispersos (Clima, Biodiversidad y Tendencias de Búsqueda) en decisiones de negocio rentables.


##  Resumen Ejecutivo 

**El Desafío:** El Hotel Coccoloba (Dibulla, La Guajira) enfrentaba tres incertidumbres críticas operando bajo "intuición":
1.  **Validación de Infraestructura:** El hotel no utiliza aire acondicionado. Se necesitaba validar si el confort térmico era viable todo el año.
2.  **Posicionamiento de Mercado:** Dibulla es un destino emergente a la sombra de Palomino (destino masivo). No existía claridad sobre la demanda real.
3.  **Producto Turístico:** Falta de inventario estructurado de biodiversidad para atraer nichos de ecoturismo.

**La Solución:** Se diseñó un pipeline de extracción de datos (ETL) utilizando fuentes abiertas (**GBIF, Open-Meteo, Google Trends**) para auditar el entorno digital y físico del hotel.


##  Hallazgos Clave 

### 1. Market Intelligence: Desacople de la Competencia
Contrario a la hipótesis inicial, la demanda de Dibulla **no depende** de Palomino.
* **Insight:** Detectamos "Océanos Azules" (Picos de demanda propios) en **Diciembre y Mayo**.
* **Acción:** Implementación de *Yield Management* (Tarifas dinámicas) para maximizar ingresos en esas ventanas exclusivas.

![Mapa de Oportunidad](outputs/figures/mapa_oportunidad_demanda.png)
*(Gráfica generada con `src/03_visualization/visualize_demand_trends.py`)*

### 2. Validación Bioclimática: El "Aire Acondicionado" Natural
Se procesaron **8,760 horas** de datos satelitales (Temperatura vs. Viento) para validar la arquitectura.
* **Insight:** Existe una correlación perfecta entre el aumento de temperatura (12:00 PM - 3:00 PM) y el aumento de la velocidad del viento (Brisas Alisios).
* **Acción:** Validación operativa de la infraestructura sostenible y protocolos de ventilación asistida solo para la franja crítica de las 16:00 horas.

![Confort Bioclimatico](outputs/figures/grafica_confort_bioclimatico.png)
*(Gráfica generada con `src/03_visualization/visualize_climate_comfort.py`)*

### 3. Estrategia de Nicho: Ciencia Ciudadana
La auditoría de biodiversidad (GBIF) reveló un sesgo del 99% en registros de una sola especie (*Tyrannus melancholicus*).
* **Estrategia:** En lugar de ver esto como "falta de datos", se diseñó el producto **"Exploradores de Coccoloba"**, incentivando a birdwatchers a visitar el hotel para completar el inventario biológico.


##  Arquitectura del Proyecto

El proyecto sigue una estructura modular escalable para análisis de datos:

```text
dibulla-hotel-analytics/
├── data/
│   ├── raw/                 # Datos crudos (GBIF, CSVs manuales) - Ignorados por Git
│   └── processed/           # Datos limpios listos para análisis
├── src/
│   ├── 01_ingestion/        # Scripts de ETL (APIs y Limpieza)
│   ├── 02_analysis/         # Lógica de negocio y estadística
│   └── 03_visualization/    # Generación de reportes gráficos
├── outputs/
│   ├── figures/             # Gráficas finales (PNG)
│   └── reports/             # Tablas resumen (Excel/CSV)
└── requirements.txt         # Dependencias del entorno
