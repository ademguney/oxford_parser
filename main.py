from parser.pdf_extractor import extract_words_from_pdf
import json

if __name__ == '__main__':
    pdf_path = "data/American_Oxford_5000.pdf"
    output_path = "data/The_Oxford_5000.json"

    print("Extracting words from PDF...")
    words = extract_words_from_pdf(pdf_path)


    print(f" Extracted {len(words)} word entries.")
    print(f" Saving to {output_path}...")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(words, f, ensure_ascii=False, indent=2)

    print("Done.")