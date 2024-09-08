from collections import Counter
from typing import List, Tuple
import emoji
import json
import logging

# Configuración básica del logger
logging.basicConfig(filename='error_log.log', level=logging.ERROR, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def q2_memory(file_path: str) -> List[Tuple[str, int]]:
    emoji_counter = Counter()
    
    # Leer el archivo línea por línea para evitar cargar todo en memoria
    with open(file_path, 'r') as file_data:
        for line in file_data:
            try:
                data = json.loads(line)
                content = data.get("content", "")
                # Contar emojis directamente si hay contenido
                if content:
                    for value in emoji.analyze(content):
                        emoji_counter[value.chars] += 1
            except (json.JSONDecodeError, KeyError) as e:
                # Manejar posibles errores en la carga de JSON y escribir en el log
                logging.error(f"Error processing line: {str(e)} - Line: {line.strip()}")
                continue
    
    # Rankear top 10 emojis más usados
    top_10_emojis = emoji_counter.most_common(10)
    
    return top_10_emojis
