import os

# Nombre del proyecto principal
project_name = "dibulla-hotel-analytics"

# Estructura de carpetas
folders = [
    f"{project_name}/data/raw",
    f"{project_name}/data/processed",
    f"{project_name}/src/01_ingestion",
    f"{project_name}/src/02_analysis",
    f"{project_name}/src/03_visualization",
    f"{project_name}/outputs/figures",
    f"{project_name}/outputs/reports"
]

# Crear carpetas
for folder in folders:
    os.makedirs(folder, exist_ok=True)
    print(f" Carpeta creada: {folder}")

# Crear archivos base
# 1. README.md
with open(f"{project_name}/README.md", "w", encoding='utf-8') as f:
    f.write(f"# Proyecto de Inteligencia de Datos: {project_name}\n\n")
    f.write("Estrategia de reactivación turística basada en datos abiertos (Open Source).\n")

# 2. .gitignore (Para no subir el archivo de 400MB a GitHub por error)
with open(f"{project_name}/.gitignore", "w", encoding='utf-8') as f:
    f.write("data/raw/*\n")        # Ignora los datos crudos pesados
    f.write("*.DS_Store\n")
    f.write("__pycache__/\n")
    f.write(".env\n")

# 3. requirements.txt
with open(f"{project_name}/requirements.txt", "w", encoding='utf-8') as f:
    f.write("pandas\nrequests\nmatplotlib\nopenmeteo-requests\n")

print("\n ¡Estructura del proyecto lista! Ahora mueve tus archivos.")