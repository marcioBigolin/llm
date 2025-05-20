from flask import Blueprint, jsonify, request

chat = Blueprint('chat', __name__)


@chat.route('/ask', methods=['POST'])
def ask():
    """
    Endpoint to handle chat messages.
    """
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({'error': 'No message provided'}), 400

    message = data['message']
    # Here you would typically process the message and generate a response
    # For now, we'll just echo the message back
    response = {
        'message': f'You said: {message}'
    }

    return jsonify(response), 200

