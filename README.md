# Analizador de Logs en Python

Herramienta de consola para analizar archivos de logs y resumir los eventos por
nivel de severidad. También cuenta las líneas mal formateadas, ignorando las
líneas vacías.

## Reglas de validación

Una línea se considera válida cuando comienza con `[INFO]`, `[WARNING]` o
`[ERROR]`, seguido de una fecha en formato ISO `YYYY-MM-DD` y un mensaje.
Además del patrón de texto, la fecha se valida con `datetime.strptime` para
descartar fechas inexistentes, como `2025-02-31`.

Se cuentan como mal formateadas las líneas que no incluyen un nivel de severidad
reconocido o que omiten la fecha, usan un formato incorrecto o contienen una
fecha inválida. Las líneas vacías o compuestas solo por espacios no se incluyen
en el total.

## Uso

Ejecuta el analizador con Python:

```bash
python3 validacion.py
```

Cuando se solicite, ingresa la ruta del archivo `.txt` que quieres analizar.
El resumen muestra el total de eventos procesados, el conteo por severidad y
las líneas mal formateadas. Si el archivo no existe, se informa el error.

## Documento de Reflexión Técnica: Analizador de Logs en Python con IA de Apoyo

**Estudiante:** Anthony Manuel Sigaran Orellana

**Entorno de desarrollo:** VS Code / Linux

**Herramientas de IA empleadas:** Gemini / VS Code Agents

### 1. Desglose de tareas: delegación a IA vs. control del desarrollador

| Componente / tarea | Herramienta utilizada | Tipo de control | Justificación técnica |
|---|---|---|---|
| Construcción de la expresión regular (`LOG_PATTERN`) | Sugerida por IA | Asistido | Se utilizó la sugerencia de una expresión regular con grupos con nombre para identificar severidad, fecha y mensaje. |
| Definición de reglas de validación | Criterio humano | 100% desarrollador | El desarrollador definió qué constituye una línea mal formateada: severidad ausente o inválida, fecha omitida o fecha que no cumple el calendario ISO. |
| Validación de calendario (`es_fecha_valida`) | Criterio humano | 100% desarrollador | Se determinó que la expresión regular por sí sola no descarta fechas inexistentes, como el 31 de febrero. Por eso se valida con `datetime.strptime`. |
| Manejo de excepciones y ruta | Sugerido por IA / validado | Mixto | Se maneja explícitamente `FileNotFoundError`, se limpian comillas adicionales de la ruta ingresada y se informa cualquier otro error inesperado. |

### 2. Criterios de conteo

- Las líneas válidas incrementan el contador de su nivel (`INFO`, `WARNING` o
  `ERROR`).
- Las líneas con severidad reconocida, pero sin fecha válida, se cuentan como
  mal formateadas y no incrementan el contador de severidad.
- Las líneas sin severidad reconocida también se cuentan como mal formateadas.
- Las líneas vacías se ignoran y no incrementan el total.
