import os
import logging
import json
import hashlib
import uuid
import re
from flask import jsonify

# Configura o logging no nível superior (apenas uma vez)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("ENY-Logger")


def ds(var):
    """
    Registra o valor de uma variável para fins de depuração.

    Args:
        var: A variável a ser registrada.
    """
    logger.info(f"    =>> {var}")


def jsonEncode(var):
    """
    Codifica uma variável em uma string JSON.

    Args:
        var: A variável a ser codificada.

    Returns:
        Uma string JSON representando a variável.
    """
    return json.dumps(var)


def jsonRequest(request, required_fields=None):
    """
    Valida uma requisição JSON, verifica os campos obrigatórios e retorna os dados.

    Args:
        request: O objeto de requisição do Flask.
        required_fields: Uma lista de nomes de campos obrigatórios (strings).

    Returns:
        Um dicionário representando os dados JSON, ou um objeto de resposta do Flask
        com uma mensagem de erro e um código de status.
    """
    if required_fields is None:
        required_fields = []

    if not request.get_json():
        return jsonify({'error': 'Invalid request format'}), 400

    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON format"}), 400

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    return data


def md5Text(text):
    """
    Calcula o hash MD5 de uma string de texto (após limpeza).

    Args:
        text: A string de texto para calcular o hash MD5.

    Returns:
        Uma string hexadecimal representando o hash MD5 do texto.
    """
    cleaned_text = text.lower().replace('?', '').replace('!', '')
    text_bytes = cleaned_text.encode()
    md5_hash = hashlib.md5(text_bytes)
    return md5_hash.hexdigest()


def uniqid():
    """
    Gera um ID único (UUID versão 4).

    Returns:
        Uma string representando o ID único gerado.
    """
    return str(uuid.uuid4())


def getFileContents(filename):
    """
    Lê todo o conteúdo de um arquivo.

    Args:
        filename: O nome do arquivo a ser lido.

    Returns:
        Uma string contendo todo o conteúdo do arquivo.
    """
    with open(filename, 'r') as file:
        return file.read()


def secure_filename(filename):
    """
    Sanitiza e valida um nome de arquivo para prevenir potenciais problemas de segurança.

    Substitui qualquer caractere não permitido por sublinhados (_), trunca o comprimento, se necessário,
    e garante que o nome do arquivo não seja muito longo ou contenha padrões suspeitos.

    Args:
        filename: O nome de arquivo original.

    Returns:
        Um nome de arquivo sanitizado e validado.
    """
    # Define um padrão de expressão regular para corresponder a caracteres não permitidos
    bad_chars = re.compile(r'[^a-zA-Z0-9_\.\-\(\)\[\]\{\}\|\?\:\;\'\"]')

    # Substitui caracteres não permitidos por sublinhados (_)
    sanitized_filename = bad_chars.sub('_', filename)

    # Trunca o comprimento, se necessário (por exemplo, para evitar nomes de arquivos excessivamente longos)
    max_length = 255
    if len(sanitized_filename) > max_length:
        sanitized_filename = sanitized_filename[:max_length]

    # Verifica se há padrões suspeitos (por exemplo, tentativas de directory traversal)
    if re.search(r'[^a-zA-Z0-9_\.]\.(?:\.\*){1,2}$', sanitized_filename):
        raise ValueError("Invalid filename: {}".format(sanitized_filename))

    return sanitized_filename
