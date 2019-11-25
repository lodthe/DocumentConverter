import werkzeug
from app import get_file_extension


def get_file_data(filename):
    with open(f'tests/sample_files/{filename}', 'rb') as file:
        return file.read()


def test_html():
    assert get_file_extension(get_file_data('HTML')) == 'html'


def test_odt():
    assert get_file_extension(get_file_data('ODT')) == 'odt'


def test_docx():
    assert get_file_extension(get_file_data('DOCX')) == 'docx'


def test_markdown():
    assert get_file_extension(get_file_data('MARKDOWN')) == 'markdown'


def test_json():
    """Should return Bad Request response cause JSON type is not available"""
    try:
        get_file_extension(get_file_data('JSON'))
    except werkzeug.exceptions.BadRequest as e:
        pass