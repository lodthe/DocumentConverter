from flask import Flask, request, send_file, abort, render_template
import pypandoc
import magic
import mimetypes
import io

from src import config

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


def convert_data(filename, file_data, input_type, output_type):
    """
    Return converted data from <input_type> format to <output_type>
    Make aborts if file formats are not available
    """
    if input_type not in config.AVAILABLE_CONVERSIONS:
        abort(400, f'Input type {input_type} is not supported.')
    if output_type not in config.AVAILABLE_CONVERSIONS[input_type]:
        abort(400, f'Conversion from {input_type} to {output_type} is not available.')

    if input_type == output_type:
        return send_file(io.BytesIO(file_data), as_attachment=True, attachment_filename=filename)

    filename_without_extension = filename
    if filename.endswith('.' + input_type):  # Remove .extension from the end of file
        filename_without_extension = filename[:-len(input_type) - 1]

    result_filename = f'{filename_without_extension}.{output_type}'
    converted_data = str.encode(pypandoc.convert(file_data, output_type, format=input_type))

    return send_file(io.BytesIO(converted_data),
                     as_attachment=True,
                     attachment_filename=result_filename)


@app.route('/convert/<output_type>', methods=['POST'])
def convert(output_type):
    if output_type not in config.TYPE_ALIAS:
        abort(400, f'Output type {output_type} is not supported.')
    if not request.files['file']:
        abort(400, f'File was not found')

    file = request.files['file']
    file_data = file.read()
    file_extension = get_file_extension(file_data)

    return convert_data(file.filename, file_data, file_extension, output_type)


@app.route('/<output_type>', methods=['GET'])
def send_file_form(output_type):
    return render_template('send_file_form.html', output_type=output_type)


@app.route('/')
def index():
    return render_template('index.html')


def create_app():
    return app