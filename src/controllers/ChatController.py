from flask import Blueprint, jsonify, request

chat = Blueprint('chat', __name__)


@chat.route('/chat', methods=['POST'])
def ask():
    """
    Endpoint to handle chat messages.
    """
    

    message = data['message']
    # Here you would typically process the message and generate a response
    # For now, we'll just echo the message back
    response = {
        'message': f'You said: {message}'
    }

    return jsonify(response), 200

