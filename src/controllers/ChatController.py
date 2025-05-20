from flask import Blueprint, jsonify, request

chat = Blueprint('chat', __name__)

from src.service import RagService #Servico de RAG


@chat.route('/chat', methods=['POST'])
def ask():
    """
    Endpoint to handle chat messages.
    """
    data = request.get_json()
    if not data or 'question' not in data:
        return jsonify({'error': 'No message provided'}), 400

    message = data['question']
    # Here you would typically process the message and generate a response
    # For now, we'll just echo the message back
    return jsonify(RagService.query(message)), 200


