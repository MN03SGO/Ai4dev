import os
import re
from datetime import datetime

# Expresión regular para extraer los tres componentes clave de la línea:
# Grupo 1 (level): INFO, WARNING o ERROR
# Grupo 2 (date): Opcional, 4 dígitos - 2 dígitos - 2 dígitos
# Grupo 3 (message): El resto del mensaje del evento
LOG_PATTERN = re.compile(
    r"^\[(?P<level>INFO|WARNING|ERROR)\]\s+(?:(?P<date>\d{4}-\d{2}-\d{2})\s+)?(?P<message>.+)$"
)

def es_fecha_valida(fecha_str: str) -> bool:
    """
    Decisión de diseño: Validar que la cadena de texto sea una fecha real en el calendario.
    """
    if not fecha_str:
        return False
    try:
        datetime.strptime(fecha_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def analizar_archivo_log(ruta_archivo: str) -> dict:
    """
    Lee el archivo de texto y calcula las estadísticas de eventos.
    """
    resumen = {
        "total": 0,
        "INFO": 0,
        "WARNING": 0,
        "ERROR": 0,
        "mal_formateadas": 0
    }

    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(f"El archivo '{ruta_archivo}' no fue encontrado.")

    with open(ruta_archivo, "r", encoding="utf-8") as file:
        for num_linea, linea in enumerate(file, 1):
            linea_limpia = linea.strip()
            
            # Caso borde: Ignorar líneas totalmente vacías
            if not linea_limpia:
                continue
            
            resumen["total"] += 1
            match = LOG_PATTERN.match(linea_limpia)

            if not match:
                # La línea no sigue el patrón base [SEVERIDAD] ...
                resumen["mal_formateadas"] += 1
                continue

            nivel = match.group("level")
            fecha_str = match.group("date")

            # Validación de fecha: Si no hay fecha o la fecha no existe en calendario
            if not fecha_str or not es_fecha_valida(fecha_str):
                resumen["mal_formateadas"] += 1
            else:
                resumen[nivel] += 1

    return resumen

def mostrar_consola(resumen: dict, ruta_archivo: str):
    """
    Muestra el resumen final estructurado en la consola.
    """
    nombre_archivo = os.path.basename(ruta_archivo)
    print("\n" + "=" * 45)
    print(f"  RESUMEN DE ANÁLISIS DE LOGS: {nombre_archivo}")
    print("=" * 45)
    print(f" Total de eventos procesados : {resumen['total']}")
    print(f"  - Eventos INFO             : {resumen['INFO']}")
    print(f"  - Eventos WARNING          : {resumen['WARNING']}")
    print(f"  - Eventos ERROR            : {resumen['ERROR']}")
    print(f"  - Líneas mal formateadas   : {resumen['mal_formateadas']}")
    print("=" * 45 + "\n")

def main():
    print("--- Analizador de Archivos de Logs ---")
    ruta = input("Ingrese la ruta del archivo .txt a analizar: ").strip()
    
    # Limpieza de comillas adicionales al arrastrar archivos en consola
    ruta = ruta.replace('"', '').replace("'", "")

    try:
        resumen = analizar_archivo_log(ruta)
        mostrar_consola(resumen, ruta)
    except FileNotFoundError as err:
        print(f"\n[ERROR DE ARCHIVO]: {err}")
    except Exception as err:
        print(f"\n[ERRORINESPERADO]: {err}")

if __name__ == "__main__":
    main()