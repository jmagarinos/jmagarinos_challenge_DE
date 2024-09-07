from collections import Counter
from typing import List, Tuple
import re
import ujson as json 

# Compilar la expresión regular una sola vez
pattern = re.compile(r'@(\w+)')

def q3_memory(file_path: str) -> List[Tuple[str, int]]:
    usernames = Counter()
    
    # Leer el archivo línea por línea para evitar cargar todo en memoria
    with open(file_path, 'r') as file:
        for line in file:
            try:
                data = json.loads(line.strip())
                if 'content' in data:
                    content = data['content']
                    # Extraer los nombres de usuario
                    usernames.update(pattern.findall(content))
            except json.JSONDecodeError:
                continue
    
    # Top 10 nombres de usuario
    top_10_usernames = usernames.most_common(10)
    
    return top_10_usernames