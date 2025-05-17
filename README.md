# Oxford Vocabulary Parser

This project aims to extract and structure English vocabulary data from two official resources:

- **The Oxford 3000** — A list of the 3000 most important English words for learners from A1 to B2 levels.
- **American Oxford 5000** — A comprehensive list covering more advanced and frequently used words (B2 and above).

The ultimate goal is to convert this raw PDF content into structured JSON format and store the parsed data into a relational database (PostgreSQL). This forms the foundational dataset for an LLM-powered Flashcard application for English learners.

---

## 🚀 Project Goals

- 📥 Extract vocabulary, word type (part of speech), and CEFR level (A1–C1) from PDF files
- 🔄 Convert to clean and structured JSON
- 🧠 (Optional Next Step) Use LLMs like GPT-4 to generate:
  - Translations
  - Most common daily-use example sentences (up to 3 per word)
- 🗃️ Store the final data into PostgreSQL for use in flashcard-based learning systems

---

## 📚 Input Files

- `The_Oxford_3000.pdf`
- `American_Oxford_5000.pdf`

These files must be placed inside the `/data` directory.

---

## 🧱 Project Structure

```bash
oxford_parser/
│
├── main.py                  # Entry point
├── parser/
│   ├── __init__.py
│   └── pdf_extractor.py     # PDF parsing logic
│
├── data/
│   ├── The_Oxford_3000.pdf
│   └── American_Oxford_5000.pdf
│
├── requirements.txt
└── README.md
