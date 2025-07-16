"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel
import pandas as pd
import re

def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.
    """

    with open("files/input/clusters_report.txt", encoding="utf-8") as file:
        lineas = file.readlines()

    contenido = lineas[4:] 

    datos = []
    fila_actual = None

    for linea in contenido:
        match = re.match(r"\s*(\d+)\s+(\d+)\s+([\d,]+)\s*%\s+(.*)", linea)
        if match:
            if fila_actual:
                fila_actual["principales_palabras_clave"] = " ".join(fila_actual["principales_palabras_clave"])
                datos.append(fila_actual)

            cluster = int(match.group(1))
            cantidad = int(match.group(2))
            porcentaje = float(match.group(3).replace(",", "."))
            palabras = match.group(4).strip()

            fila_actual = {
                "cluster": cluster,
                "cantidad_de_palabras_clave": cantidad,
                "porcentaje_de_palabras_clave": porcentaje,
                "principales_palabras_clave": [palabras]
            }
        else:
            if fila_actual:
                fila_actual["principales_palabras_clave"].append(linea.strip())

    if fila_actual:
        fila_actual["principales_palabras_clave"] = " ".join(fila_actual["principales_palabras_clave"])
        datos.append(fila_actual)

    for fila in datos:
        palabras = fila["principales_palabras_clave"]
        palabras = " ".join(palabras.split())             
        palabras = palabras.rstrip(".")                    
        palabras = palabras.replace(", ", ",")            
        palabras = palabras.replace(",", ", ")          
        fila["principales_palabras_clave"] = palabras

    # DataFrame
    df = pd.DataFrame(datos)
    df.columns = [col.lower().replace(" ", "_") for col in df.columns]

    return df