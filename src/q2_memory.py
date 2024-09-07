from collections import Counter
from typing import List, Tuple
import emoji
import json

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
            except (json.JSONDecodeError, KeyError):
                # Manejar posibles errores en la carga de JSON
                continue
    
    # Rankear top 10 emojis más usados
    top_10_emojis = emoji_counter.most_common(10)
    
    return top_10_emojis