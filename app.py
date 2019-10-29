from flask import Flask, request, send_file, abort
import pypandoc
import magic
import mimetypes
import io
import os

app = Flask(__name__)

# File extension aliases
TYPE_ALIAS = {
    'htm': 'html',
    'html': 'html',
    'docx': 'docx',
    'markdown': 'markdown',
    'odt': 'odt',
    'bat': 'markdown',
    'plain': 'plain',
}

# Conversion: key = input format, value = available output formats
AVAILABLE_CONVERSIONS = {
    'html': ('html', 'markdown', 'plain'),
    'markdown': ('markdown', 'html', 'plain'),
    'docx': ('docx', 'html', 'markdown', 'plain'),
    'odt': ('odt', 'html', 'markdown', 'plain'),
}


def get_file_extension(file_data):
    try:
        file_mime = magic.from_buffer(file_data, mime=True)
        file_extension = mimetypes.guess_extension(file_mime)[1:]
    except Exception:
        abort(400, 'Can\'t identify the file format.')

    if file_extension not in TYPE_ALIAS:
        abort(400, f'Input type {file_extension} is not supported.')

    return TYPE_ALIAS[file_extension]


def convert_data(filename, file_data, input_type, output_type):
    """
    Return converted data from <input_type> format to <output_type>
    Make aborts if file formats are not available
    """
    if input_type not in AVAILABLE_CONVERSIONS:
        abort(400, f'Input type {input_type} is not supported.')
    if output_type not in AVAILABLE_CONVERSIONS[input_type]:
        abort(400, f'Conversion from {input_type} to {output_type} is not available.')

    # Return the same data, if output format is equal to input format
    if input_type == output_type:
        return send_file(io.BytesIO(file_data),
                         mimetype=mimetypes.guess_type(filename)[0],
                         as_attachment=True,
                         attachment_filename=filename)

    filename_without_extension = filename
    if filename.endswith('.' + input_type): # Remove .extension from the end of file
        filename_without_extension = filename[:-len(input_type) - 1]

    result_filename = f'{filename_without_extension}.{output_type}'
    converted_data = str.encode(pypandoc.convert(file_data, output_type, format=input_type))

    return send_file(io.BytesIO(converted_data),
                     mimetype=mimetypes.guess_type(result_filename)[0],
                     as_attachment=True,
                     attachment_filename=result_filename)


@app.route('/convert/<output_type>', methods=['GET', 'POST'])
def convert(output_type):
    if output_type not in TYPE_ALIAS:
        abort(400, f'Output type {output_type} is not supported.')

    if request.method == 'POST':
        file = request.files['file']

        if file:
            file_data = file.read()
            file_extension = get_file_extension(file_data)

            return convert_data(file.filename, file_data, file_extension, output_type)

    # On GET query return form that allows to send a file
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
         <input type=file name=file> <br>
         <input type=submit value=Upload>
    </form>
    '''


if __name__ == '__main__':
    app.run(host=os.getenv('DC_HOST'), port=os.getenv('DC_PORT'))
