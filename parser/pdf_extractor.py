import pdfplumber
import re
from collections import defaultdict


def extract_words_from_pdf(pdf_path: str):
    """
        Extracts words, their parts of speech, and CEFR levels from an Oxford vocabulary PDF.

        The function reads lines like:
            "back n., adv. A1, adj. A2, v. B2"
        and converts them into a structured list like:
            {
                "word": "back",
                "parts": [
                    {"part_of_speech": "n", "level": "A1"},
                    {"part_of_speech": "adv", "level": "A1"},
                    {"part_of_speech": "adj", "level": "A2"},
                    {"part_of_speech": "v", "level": "B2"}
                ]
            }

        Args:
            pdf_path (str): Path to the PDF file.

        Returns:
            List[dict]: A list of dictionaries containing word data with part of speech and level info.
        """

    word_dict = defaultdict(list)
    entry_pattern = re.compile(r"^(?P<word>[a-zA-Z\-']+)\s+(?P<info>.+)$")

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue

            lines = text.split('\n')
            for line in lines:
                line = line.strip()

                if len(line) < 5 or "oxford" in line.lower() or re.match(r"^\d+/\d+$", line):
                    continue

                match = entry_pattern.match(line)
                if not match:
                    continue

                word = match.group("word")
                info = match.group(2)
                tokens = [i.strip() for i in info.split(",")]

                for token in tokens:
                    parts = token.split()
                    if len(parts) == 2:
                        pos = parts[0].replace(".", "").lower()
                        level = parts[1].strip().upper()
                        word_dict[word].append({
                            "part_of_speech": pos,
                            "level": level
                        })

    final_list = []
    for word, parts in word_dict.items():
        final_list.append({
            "word": word,
            "parts": parts
        })

    return final_list