import os
from enum import nonmember
import pytest
from parser.pdf_extractor import extract_words_from_pdf



# --- Fixture to provide sample PDF ---
@pytest.fixture
def sample_pdf_path():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(base_dir, "data", "The_Oxford_3000.pdf")



# --- 1. PDF parsing returns non-empty list ---
def test_pdf_parsing_success(sample_pdf_path):
    results = extract_words_from_pdf(sample_pdf_path)
    assert isinstance(results, list)
    assert len(results) > 0, "No words could be extracted from the PDF"


# --- 2. Is the word 'back' on the list? ---
def test_word_entry_exist(sample_pdf_path):
    results = extract_words_from_pdf(sample_pdf_path)
    entry = next((e for e in results if e["word"]=="back"), None)
    assert entry is not None, "No entry found for word 'back'"



# --- 3. Are the part/level matches of the word 'back' correct ---
def test_word_entry_back_parts(sample_pdf_path):
    results = extract_words_from_pdf(sample_pdf_path)
    entry = next((e for e in results if e["word"]=="back"), None)
    assert entry is not None, "No entry found for word 'back'"

    expected_parts = {
        ("n.", "A1"),
        ("adv.", "A1"),
        ("adj.", "A2"),
        ("v.", "B2")
    }

    actual_parts = {(p["part_of_speech"], p["level"]) for p in entry["parts"]}
    for expected in expected_parts:
        assert expected in actual_parts, f"Expected {expected} but got {actual_parts}"


# --- 4. Are multiple words like 'a' and 'an' parsed? ---
def test_multiple_base_words(sample_pdf_path):
    results = extract_words_from_pdf(sample_pdf_path)

    a_entry = next((e for e in results if e["word"]=="a"), None)
    an_entry = next((e for e in results if e["word"] == "an"), None)

    assert a_entry is not None, "No entry found for word 'a'"
    assert an_entry is not None, "No entry found for word 'an'"

    assert any(p["level"] == "A1" and p["part_of_speech"] == "article" for p in a_entry["parts"])
    assert any(p["level"] == "A1" and p["part_of_speech"] == "article" for p in an_entry["parts"])




# --- 5. The same word|pos|level combinations should not be added again.  ---
def test_duplicate_entries_filtered(sample_pdf_path):
    results = extract_words_from_pdf(sample_pdf_path)
    seen = set()
    for entry in results:
        for p in entry["parts"]:
            key = f"{entry['word']}|{p['part_of_speech']}|{p['level']}"
            assert key not in seen, f"Duplicate entry found: {key}"
            seen.add(key)