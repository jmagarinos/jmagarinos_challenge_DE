from collections import Counter
from typing import List, Tuple
import ujson as json  # Usar ujson para un análisis JSON más rápido
import emoji
from concurrent.futures import ThreadPoolExecutor

# Función para procesar un grupo de líneas y contar emojis
def process_lines(lines: List[str]) -> Counter:
    emoji_counter = Counter()
    for line in lines:
        try:
            data = json.loads(line)
            content = data.get("content", "")
            if content:
                for value in emoji.analyze(content):
                    emoji_counter[value.chars] += 1
        except (json.JSONDecodeError, KeyError):
            continue
    return emoji_counter

def q2_time(file_path: str) -> List[Tuple[str, int]]:
    # Leer el archivo línea por línea
    with open(file_path, 'r') as file_data:
        lines = file_data.readlines()
    
    # Dividir las líneas en grupos para procesamiento en paralelo
    num_threads = 24  # Ajustar basado en el número de núcleos de CPU
    total_lines = len(lines)
    chunk_size = (total_lines // num_threads) + (total_lines % num_threads > 0)  # Redondear hacia arriba
    
    # Usar ThreadPoolExecutor para paralelizar el procesamiento de líneas
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(process_lines, lines[i:i + chunk_size]) for i in range(0, total_lines, chunk_size)]
    
    # Reunir los resultados de todos los hilos
    total_counter = Counter()
    for future in futures:
        total_counter.update(future.result())
    
    # Clasificar los 10 emojis más usados
    top_10_emojis = total_counter.most_common(10)
    
    return top_10_emojis