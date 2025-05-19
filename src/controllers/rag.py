from flask import request, jsonify, Blueprint


rag = Blueprint('rag', __name__)


@rag.route('/treinar', methods=['POST'])
def upload():
    """
    Endpoint to upload a file.
    """
    if 'arquivo' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    arquivo = request.files['arquivo']

    if arquivo.filename == '':
        return jsonify({'error': 'No selected file'}), 400


    return jsonify({'filename': arquivo.filename}), 200