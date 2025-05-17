from parser.pdf_extractor import extract_words_from_pdf
import os

def test_extract_words_from_sample_pdf():
    # Get the absolute path to the test PDF
    base_dir = os.path.dirname(os.path.dirname(__file__))
    pdf_path = os.path.join(base_dir, "data", "test_page.pdf")
    sample_result = extract_words_from_pdf(pdf_path)

    expected_word = "back"
    required_parts = {"adv": "A1", "adj": "A2", "v": "B2"}

    # Find the word entry with 'back'
    back_entry = next((item for item in sample_result if item["word"].lower() == expected_word), None)
    assert back_entry is not None, "'back' word not found in parsed results"

    # Create a dict for actual part-of-speech to level mapping
    actual_parts_dict = {p["part_of_speech"]: p["level"] for p in back_entry["parts"]}

    # Verify that each required part is present with the correct level
    for pos, level in required_parts.items():
        assert pos in actual_parts_dict, f"'{pos}' not found in parts"
        assert actual_parts_dict[pos] == level, f"Level mismatch for '{pos}': expected {level}, got {actual_parts_dict[pos]}"
