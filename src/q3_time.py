from collections import Counter
from typing import List, Tuple
import re
import ujson as json 

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
            except json.JSONDecodeError:
                continue

def q3_time(file_path: str) -> List[Tuple[str, int]]:
    usernames = Counter(process_file(file_path))
    
    # Top 10 nombres de usuario
    top_10_usernames = usernames.most_common(10)
    
    return top_10_usernames