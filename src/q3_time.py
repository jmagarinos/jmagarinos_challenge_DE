from collections import Counter
from typing import List, Tuple
import re
import ujson as json
import logging

# Configuración básica del logger
logging.basicConfig(filename='error_log.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Compilar la expresión regular una sola vez
pattern = re.compile(r'@(\w+)')

def process_file(file_path: str):
    with open(file_path, 'r') as file:
        for line in file:
            try:
                data = json.loads(line.strip())
                if 'content' in data:
                    content = data['content']
                    # Extraer los nombres de usuario
                    yield from pattern.findall(content)
            except json.JSONDecodeError as e:
                # Manejar errores de decodificación JSON y escribir en log
                logging.error(f"Error processing line: {str(e)} - Line: {line.strip()}")
                continue

def q3_time(file_path: str) -> List[Tuple[str, int]]:
    usernames = Counter(process_file(file_path))
    
    # Top 10 nombres de usuario
    top_10_usernames = usernames.most_common(10)
    
    return top_10_usernames
