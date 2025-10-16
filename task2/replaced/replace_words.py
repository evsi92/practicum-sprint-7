import os
import re
from pathlib import Path

def load_dictionary(dict_path):
    mappings = []
    with open(dict_path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or '|' not in line:
                continue
            old, new = line.split('|', 1)
            mappings.append((old, new))
    return mappings

def case_preserving_replace(text, old, new):
    pattern = re.compile(re.escape(old), re.IGNORECASE)

    def repl(match):
        word = match.group(0)
        # Match case style of the original
        if word.isupper():
            return new.upper()
        elif word.islower():
            return new.lower()
        elif word[0].isupper() and word[1:].islower():
            return new.capitalize()
        else:
            # Mixed case: try to preserve character-by-character
            return ''.join(
                n.upper() if o.isupper() else n.lower()
                for o, n in zip(word, new.ljust(len(word), new[-1])))

    return pattern.sub(repl, text)

def process_file(file_path, mappings):
    with open(file_path, encoding='utf-8') as f:
        content = f.read()
    for old, new in mappings:
        content = case_preserving_replace(content, old, new)
        content = remove_square_bracket_numbers(content)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def remove_square_bracket_numbers(text):
    # Removes things like [12], [1], [123]
    return re.sub(r'\[\d+\]', '', text)

def main():
    base_dir = Path(__file__).parent
    dict_path = base_dir / 'dictionary.txt'
    mappings = load_dictionary(dict_path)
    # List all .txt files except dictionary.txt and files in dictionary/
    for file in base_dir.glob('*.txt'):
        if file.name == 'dictionary.txt':
            continue
        print(f'Processing {file.name}...')
        process_file(file, mappings)
    # Optionally process files in subdirectories (except dictionary/)
    for sub in base_dir.iterdir():
        if sub.is_dir() and sub.name != 'dictionary':
            for file in sub.glob('*.txt'):
                print(f'Processing {file}...')
                process_file(file, mappings)

if __name__ == '__main__':
    main()

