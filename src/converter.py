from flask import send_file, abort
import pypandoc
import io

import config

def convert_data(filename, file_data, input_type, output_type):
    """
    Converts the given data from <input_type> to the <output_type>.
    It aborts if file formats are not supported.
    """
    if input_type not in config.AVAILABLE_CONVERSIONS:
        abort(400, f'Input type {input_type} is not supported.')
    if output_type not in config.AVAILABLE_CONVERSIONS[input_type]:
        abort(400, f'Conversion from {input_type} to {output_type} is not supported.')

    if input_type == output_type:
        return send_file(io.BytesIO(file_data), as_attachment=True, attachment_filename=filename)

    filename_without_extension = filename
    if filename.endswith('.' + input_type):  # Remove .extension from the end of the file
        filename_without_extension = filename[:-len(input_type) - 1]

    result_filename = f'{filename_without_extension}.{output_type}'
    converted_data = str.encode(pypandoc.convert(file_data, output_type, format=input_type))

    return send_file(io.BytesIO(converted_data),
                     as_attachment=True,
                     attachment_filename=result_filename)