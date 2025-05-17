import pdfplumber
import re
import unicodedata
from typing import List, Dict

def clean_text(text: str) -> str:
    """
    Clean whitespace, normalize unicode, remove non-printables.
    """
    text = re.sub(r'\s+', ' ', text).strip()
    text = ''.join(ch for ch in text if ch.isprintable())
    text = unicodedata.normalize('NFKC', text)
    return text

def is_valid_word(word: str) -> bool:
    """
    Accept lowercase alphabetic words, 1-20 characters (to include 'a', 'i').
    """
    return re.match(r'^[a-z]+$', word) and 1 <= len(word) <= 20

def extract_words_from_pdf(pdf_path: str) -> List[Dict]:
    """
    Extracts dictionary entries with word, CEFR level, and parts of speech,
    preserving part-of-speech and level pairings.
    """
    word_entries = []
    seen_entries = set()

    # Composite pattern: (pos. level) e.g., "adj. A2"
    entry_pattern = re.compile(
        r'\b(n\.|v\.|adj\.|adv\.|exclam\.|modal v\.|prep\.|conj\.|pron\.|article)\s+(A1|A2|B1|B2|C1|C2)\b',
        re.IGNORECASE
    )

    with pdfplumber.open(pdf_path, laparams={'detect_vertical': True, 'all_texts': True}) as pdf:
        for page in pdf.pages:
            text = page.extract_text(x_tolerance=2, y_tolerance=2, layout=True, use_text_flow=True)
            if not text:
                continue

            lines = text.split('\n')

            for line in lines:
                line = clean_text(line)
                if len(line) < 3 or "oxford" in line.lower() or re.match(r"^\d+/\d+$", line):
                    continue

                blocks = re.split(r'\s{2,}|\t+', line)
                for block in blocks:
                    block = clean_text(block)
                    if not block:
                        continue

                    parts = block.split()
                    if not parts:
                        continue

                    # Handle multiple base words e.g. "a, an article A1"
                    raw_words = parts[0].split(",")
                    base_words = [w.strip().lower() for w in raw_words if is_valid_word(w.strip().lower())]

                    matches = entry_pattern.findall(block)

                    if base_words and matches:
                        for word in base_words:
                            parts_data = []
                            for pos, level in matches:
                                key = f"{word}|{pos.lower()}|{level.upper()}"
                                if key not in seen_entries:
                                    seen_entries.add(key)
                                    parts_data.append({
                                        "part_of_speech": pos.lower(),
                                        "level": level.upper()
                                    })

                            if parts_data:
                                word_entries.append({
                                    "word": word,
                                    "parts": parts_data
                                })

    return word_entries
