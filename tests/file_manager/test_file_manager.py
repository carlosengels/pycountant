from app.services.file_manager import get_next_pdf, get_all_pdf
from app.core.config import INPUT_DIR

def test_get_next_pdf():
    test_file = INPUT_DIR / "statement_january.pdf"
    test_file.touch()

    result = get_next_pdf()

    assert result is not None
    assert result.name == "statement_january.pdf"
    assert result.exists()

    test_file.unlink()

def test_get_all_pdf_multiple_pdfs():
    test_file_1 = INPUT_DIR / "test_file_1.pdf"
    test_file_1.touch()
    test_file_2 = INPUT_DIR / "test_file_2.pdf"
    test_file_2.touch()
    test_file_3 = INPUT_DIR / "test_file_3.pdf"
    test_file_3.touch()
    result = get_all_pdf()

    assert result is not None
    assert len(result) == 3

    test_file_1.unlink()
    test_file_2.unlink()
    test_file_3.unlink()