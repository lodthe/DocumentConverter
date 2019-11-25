import pytest

import io
from app import create_app


@pytest.fixture
def app():
    app = create_app()
    app.testing = True

    return app


@pytest.fixture
def client(app):
    return app.test_client()


def get_file_data(filename):
    with open(f'tests/sample_files/{filename}', 'rb') as file:
        return file.read()


def get_response(filename, output_type, client):
    response = client.post(
        f'/convert/{output_type}',
        data={
            'file': (io.BytesIO(get_file_data(filename)), filename)
        },
        content_type='multipart/form-data'
    )

    return response


def test_conversion_input_format_is_output_format(client):
    assert get_file_data('HTML') == get_response('HTML', 'html', client).data
    assert get_file_data('MARKDOWN') == get_response('MARKDOWN', 'markdown', client).data
    assert get_file_data('DOCX') == get_response('DOCX', 'docx', client).data
    assert get_file_data('ODT') == get_response('ODT', 'odt', client).data


def test_to_html(client):
    assert get_file_data('MARKDOWN.html') == get_response('MARKDOWN', 'html', client).data
    assert get_file_data('DOCX.html') == get_response('DOCX', 'html', client).data
    assert get_file_data('ODT.html') == get_response('ODT', 'html', client).data


def test_to_markdown(client):
    assert get_file_data('HTML.markdown') == get_response('HTML', 'markdown', client).data
    assert get_file_data('DOCX.markdown') == get_response('DOCX', 'markdown', client).data
    assert get_file_data('ODT.markdown') == get_response('ODT', 'markdown', client).data


def test_wrong_output_format(client):
    assert get_response('HTML', 'undefined_format', client).status_code == 400
