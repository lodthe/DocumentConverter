from flask import Flask, request, send_file, abort
import pypandoc
import magic
import mimetypes
import io
import os

app = Flask(__name__)

TYPE_ALIAS = {
    'htm': 'html',
    'html': 'html',
    'docx': 'docx',
    'markdown': 'markdown',
    'odt': 'odt'
}

@app.route('/convert/<output_type>', methods=['GET', 'POST'])
def convert(output_type):
    if output_type not in TYPE_ALIAS:
        abort(400, f'Output type {output_type} is not supported.')

    if request.method == 'POST':
        file = request.files['file']

        if file:
            try:
                file_data = file.read()
                file_mime = magic.from_buffer(file_data, mime=True)
                file_extension = mimetypes.guess_extension(file_mime)[1:]
            except Exception:
                abort(500, 'Can\'t identify file format.')

            if file_extension not in TYPE_ALIAS:
                abort(400, f'File type {file_extension} is not supported.')

            file_extension = TYPE_ALIAS[file_extension]

            filename_without_extension = file.filename

            if file.filename.endswith('.' + file_extension):
                filename_without_extension = file.filename[:-len(file_extension) - 1]

            result_filename = f'{filename_without_extension}.{output_type}'
            converted_data = str.encode(pypandoc.convert(file_data,
                                                         output_type,
                                                         format=file_extension))

            return send_file(io.BytesIO(converted_data),
                             mimetype=mimetypes.guess_type(result_filename)[0],
                             as_attachment=True,
                             attachment_filename=result_filename)

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
