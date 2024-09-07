from typing import List, Tuple
from datetime import datetime
import pandas as pd
import json

def q1_memory(file_path: str) -> List[Tuple[datetime.date, str]]:
    # Leer el archivo JSON línea por línea y procesarlo
    data = []
    with open(file_path, 'r') as json_file:
        for line in json_file:
            try:
                item = json.loads(line.strip())
                # Verificar que los campos necesarios están presentes antes de agregar
                if 'date' in item and 'user' in item and 'id' in item:
                    data.append((item['date'], item['user']['username']))
            except json.JSONDecodeError:
                # Manejar errores de decodificación JSON
                continue
    
    # Convertir la lista de tuplas en un DataFrame de pandas
    df = pd.DataFrame(data, columns=['date', 'user'])
    
    # Convertir el campo 'date' a formato datetime directamente sin conversiones intermedias
    df['date'] = pd.to_datetime(df['date']).dt.date

    # Calcular la cantidad de tweets por fecha y encontrar las 10 fechas con más tweets
    tweet_counts = df['date'].value_counts().nlargest(10)
    top_10_dates = tweet_counts.index

    # Filtrar el DataFrame para incluir solo las fechas top 10
    df_top_10 = df[df['date'].isin(top_10_dates)]
    
    # Encontrar el usuario con más tweets para cada una de las fechas top 10
    top_users = df_top_10.groupby('date')['user'].agg(lambda x: x.value_counts().idxmax())

    # Convertir el resultado a una lista de tuplas con (fecha, usuario)
    result = [(date, user) for date, user in zip(top_10_dates, top_users)]
    
    return result