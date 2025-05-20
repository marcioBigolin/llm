from flask import request, jsonify, Blueprint
import util.Eny as Eny

from src.service import RagService #Servico de RAG

rag = Blueprint('rag', __name__)


@rag.route('/treinar', methods=['POST'])
def upload():
    """
    Endpoint to upload a file.
    """
    if 'arquivo' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    arquivo = request.files['arquivo']
    file = Eny.moveUploadedFile(arquivo, 'cache/' + arquivo.filename) #mover 

    RagService.treinarArquivo(file)

    if arquivo.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    

    return jsonify({'filename': arquivo.filename}), 200