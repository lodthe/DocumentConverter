import pytest

import requests


def get_file_data(filename):
    with open(f'tests/sample_files/{filename}', 'rb') as file:
        return file.read()


def get_response(filename, output_type):
    URL = f'http://127.0.0.1:5000/convert/{output_type}'
    FILES = {
        'file': get_file_data(filename)
    }

    return requests.post(url=URL, files=FILES)


def test_conversion_input_format_is_output_format():
    assert get_file_data('HTML') == get_response('HTML', 'html').content
    assert get_file_data('MARKDOWN') == get_response('MARKDOWN', 'markdown').content
    assert get_file_data('DOCX') == get_response('DOCX', 'docx').content
    assert get_file_data('ODT') == get_response('ODT', 'odt').content


def test_to_html():
    assert get_file_data('MARKDOWN.html') == get_response('MARKDOWN', 'html').content
    assert get_file_data('DOCX.html') == get_response('DOCX', 'html').content
    assert get_file_data('ODT.html') == get_response('ODT', 'html').content


def test_to_markdown():
    assert get_file_data('HTML.markdown') == get_response('HTML', 'markdown').content
    assert get_file_data('DOCX.markdown') == get_response('DOCX', 'markdown').content
    assert get_file_data('ODT.markdown') == get_response('ODT', 'markdown').content


def test_from_json():
    assert get_response('JSON', 'html').status_code == 400

def test_wrong_output_format():
    assert get_response('HTML', 'undefined_format').status_code == 400
