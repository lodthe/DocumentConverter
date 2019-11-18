from flask import Flask, request, abort, render_template
import magic
import mimetypes
import json

from src import config, converter

app = Flask(__name__)

def get_file_extension(file_data):
    try:
        file_mime = magic.from_buffer(file_data, mime=True)
        file_extension = mimetypes.guess_extension(file_mime)[1:]
    except:
        abort(400, 'Can\'t identify the file format.')

    if file_extension not in config.TYPE_ALIAS:
        abort(400, f'Input type {file_extension} is not supported.')

    return config.TYPE_ALIAS[file_extension]


@app.route('/convert/<output_type>', methods=['POST'])
def convert(output_type):
    if output_type not in config.TYPE_ALIAS:
        abort(400, f'Output type {output_type} is not supported.')
    if not request.files['file']:
        abort(400, f'File was not found')

    file = request.files['file']
    file_data = file.read()
    file_extension = get_file_extension(file_data)

    return converter.convert_data(file.filename, file_data, file_extension, output_type)


@app.route('/<output_type>', methods=['GET'])
def send_file_form(output_type):
    return render_template('send_file_form.html', output_type=output_type)

@app.route('/get_available_conversions')
def get_available_conversions():
    return json.dumps(config.AVAILABLE_CONVERSIONS)


@app.route('/')
def index():
    return render_template('index.html')  # change templates/index.html


def create_app():
    return app