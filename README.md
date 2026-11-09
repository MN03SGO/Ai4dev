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

## 2. Ejemplo concreto: corrección de una sugerencia incompleta de la IA

### Sugerencia inicial

Al solicitar una forma rápida de separar los componentes de cada línea, una
propuesta inicial fue usar manipulación básica de cadenas con `.split()`:

```python
partes = linea.split(" ")
severidad = partes[0].replace("[", "").replace("]", "")
fecha = partes[1]
mensaje = " ".join(partes[2:])
```

### Detección del fallo y corrección

Este enfoque supone que todas las líneas tienen una fecha en la posición
`partes[1]`. En una línea como `[WARNING] Invalid password attempt`, ese
elemento sería `"Invalid"`, no una fecha. Además, el resultado depende de que
los componentes estén separados por exactamente un espacio. Si se intenta
validar ese valor como fecha, puede causar una excepción si no se maneja o una
clasificación incorrecta.

Se sustituyó esa división posicional por la expresión regular `LOG_PATTERN`,
que captura la severidad, una fecha opcional y el mensaje mediante grupos con
nombre. La fecha opcional permite reconocer el registro y luego clasificarlo
como mal formateado cuando `es_fecha_valida()` recibe un valor vacío. Las fechas
presentes se validan con `datetime.strptime`.

## 3. Evidencia y análisis de resultados de pruebas

### Prueba 1: archivo bien formado (`logs_validos.txt`)

- **Entrada:** 4 registros con severidades `INFO`, `WARNING` y `ERROR`, y fechas
  válidas en formato `YYYY-MM-DD`.
- **Resultado esperado:** 4 eventos procesados y 0 líneas mal formateadas.
- **Resultado obtenido:**

```text
=============================================
  RESUMEN DE ANÁLISIS DE LOGS: logs_validos.txt
=============================================
 Total de eventos procesados : 4
  - Eventos INFO             : 2
  - Eventos WARNING          : 1
  - Eventos ERROR            : 1
  - Líneas mal formateadas   : 0
=============================================
```

### Prueba 2: archivo inconsistente (`logs_incosistentes.txt`)

- **Entrada:** 5 registros con distintos casos borde:
  1. `[INFO] 2025-01-10 User logged in` (válido).
  2. `[WARNING] Invalid password attempt` (sin fecha).
  3. `[ERROR] 2025-02-31 Invalid leap date connection error` (fecha inexistente).
  4. `[TRACE] 2025-01-10 Unknown severity level` (severidad no permitida).
  5. `[ERROR] 2025-01-15 Timeout waiting for server response` (válido).
- **Resultado esperado:** 5 eventos procesados, 1 `INFO`, 0 `WARNING`, 1
  `ERROR` y 3 líneas mal formateadas.
- **Resultado obtenido:**

```text
=============================================
  RESUMEN DE ANÁLISIS DE LOGS: logs_incosistentes.txt
=============================================
 Total de eventos procesados : 5
  - Eventos INFO             : 1
  - Eventos WARNING          : 0
  - Eventos ERROR            : 1
  - Líneas mal formateadas   : 3
=============================================
```

## 4. Aprendizaje sobre el uso de la IA como herramienta de apoyo

El desarrollo de este analizador mostró que las herramientas de IA pueden
acelerar la generación de sintaxis repetitiva y proponer estructuras iniciales,
como expresiones regulares. Sin embargo, esas propuestas deben contrastarse con
las reglas del problema y probarse con casos borde.

El criterio técnico del desarrollador sigue siendo indispensable para:

1. **Establecer los límites de validación:** definir qué datos se consideran
   válidos según los requisitos.
2. **Auditar el código generado:** probarlo con entradas mal formateadas y
   detectar supuestos que no cubren todos los casos.
3. **Garantizar la solidez del sistema:** revisar y adaptar las sugerencias para
   que el comportamiento final sea consistente con los requisitos.
