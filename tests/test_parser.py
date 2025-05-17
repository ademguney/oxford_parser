from parser.pdf_extractor import extract_words_from_pdf

def test_extract_words_from_sample_pdf():
    # a small sample PDF file or a ready sample text content is required for testing.
    # but since pdfplumber expects a direct PDF file, this test should be done with
    # a real small test.pdf file
    # For now, I am providing a sample output control to test the structure

    result = [
        {
            "word": "back",
            "parts": [
                {"part_of_speech": "n", "level": "A1"},
                {"part_of_speech": "adv", "level": "A1"},
                {"part_of_speech": "adj", "level": "A2"},
                {"part_of_speech": "v", "level": "B2"}
            ]
        }
    ]

    sample_tesult = extract_words_from_pdf()