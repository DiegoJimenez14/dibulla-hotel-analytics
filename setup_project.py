import os


project_name = "dibulla-hotel-analytics"


folders = [
    f"{project_name}/data/raw",
    f"{project_name}/data/processed",
    f"{project_name}/src/01_ingestion",
    f"{project_name}/src/02_analysis",
    f"{project_name}/src/03_visualization",
    f"{project_name}/outputs/figures",
    f"{project_name}/outputs/reports"
]


for folder in folders:
    os.makedirs(folder, exist_ok=True)
    print(f" Carpeta creada: {folder}")


with open(f"{project_name}/README.md", "w", encoding='utf-8') as f:
    f.write(f"# Proyecto de Inteligencia de Datos: {project_name}\n\n")
    f.write("Estrategia de reactivación turística basada en datos abiertos (Open Source).\n")


with open(f"{project_name}/.gitignore", "w", encoding='utf-8') as f:
    f.write("data/raw/*\n")        # Ignora los datos crudos pesados
    f.write("*.DS_Store\n")
    f.write("__pycache__/\n")
    f.write(".env\n")


with open(f"{project_name}/requirements.txt", "w", encoding='utf-8') as f:
    f.write("pandas\nrequests\nmatplotlib\nopenmeteo-requests\n")

print("\n ¡Estructura del proyecto lista! Ahora mueve tus archivos.")
