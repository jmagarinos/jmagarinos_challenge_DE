import pandas as pd
import ujson
from typing import List, Tuple
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# Función para analizar un bloque de líneas del archivo JSON
def parse_json_lines(lines: List[str]) -> List[Tuple[str, str]]:
    result = []
    for line in lines:
        try:
            # Intenta cargar el JSON de la línea
            item = ujson.loads(line.strip())
            # Verifica que los campos necesarios estén presentes antes de agregar
            if 'date' in item and 'user' in item and 'id' in item:
                result.append((item['date'], item['user']['username']))
        except ValueError:
            # Maneja errores de decodificación JSON
            continue
    return result

# Función para paralelizar la lectura y procesamiento del archivo
def q1_time(file_path: str) -> List[Tuple[datetime.date, str]]:
    # Lee el archivo en memoria
    with open(file_path, 'r') as json_file:
        lines = json_file.readlines()

    # Divide las líneas en bloques para procesamiento paralelo
    num_threads = 16  # Ajustar basado en la cantidad de núcleos de CPU
    chunk_size = len(lines) // num_threads
    
    # Usa ThreadPoolExecutor para paralelizar el análisis del JSON
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Envía tareas para procesar cada bloque de líneas en paralelo
        futures = [executor.submit(parse_json_lines, lines[i:i + chunk_size]) for i in range(0, len(lines), chunk_size)]
    
    # Recoge los resultados de todos los hilos
    data = []
    for future in futures:
        data.extend(future.result())

    # Convierte la lista de tuplas en un DataFrame
    df = pd.DataFrame(data, columns=['date', 'user'])
    
    # Convierte la columna 'date' a formato datetime.date
    df['date'] = pd.to_datetime(df['date']).dt.date

    # Obtiene las 10 fechas con más tweets
    tweet_counts = df['date'].value_counts().nlargest(10)
    top_10_dates = tweet_counts.index

    # Filtra el DataFrame para incluir solo las fechas top 10
    df_top_10 = df[df['date'].isin(top_10_dates)]

    # Encuentra el usuario con más tweets para cada una de las fechas top 10
    top_users = df_top_10.groupby('date')['user'].agg(lambda x: x.value_counts().idxmax())

    # Convierte el resultado a una lista de tuplas (fecha, usuario)
    result = [(date, user) for date, user in zip(top_10_dates, top_users)]
    
    return result