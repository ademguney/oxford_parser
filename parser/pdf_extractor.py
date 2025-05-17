import pdfplumber
import re

def extract_words_from_pdf(pdf_path: str):
    word_entries=[]
    entry_pattern = re.compile(r"(?P<word>^[a-zA-Z\-']+)\s+(?P<info>.+)")

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue

            lines = text.split('\n')
            for line in lines:
                line = line.strip()
                match = entry_pattern.match(line)
                if not match:
                    continue

            word = match.group('word')
            info = match.group('info')
            tokens = [i.strip() for i in info.split(',')]

            for token in tokens:
                parts = token.split()
                if len(parts) < 2:
                    part_of_speech = parts[0].replace(".", "")
                    level = parts[1]
                    word_entries.append({
                        "word": word,
                        "part_of_speech": part_of_speech,
                        "level": level
                    })

    return word_entries
