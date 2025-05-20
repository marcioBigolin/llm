"""
    Módulo para definir os modelos de LLM (Large Language Model) a serem utilizados.
    Este módulo contém funções para retornar instâncias de modelos LLM específicos,
    incluindo Google Gemini e OpenAI. Para essa demo deixei apenas o Google Gemini.
    O módulo também inclui uma função para retornar o modelo de embedding do Google Gemini.

    As funções disponíveis são:
        - googleLLM: Retorna uma instância do modelo Google Gemini (Engenharia de prompt).
        - gptLLM: Retorna uma instância do modelo LLM do OpenAI (Engenharia de prompt).
        - embbedLLM: Retorna uma instância do modelo de embedding especificado.
        - llm: Retorna uma instância do modelo LLM especificado (Google Gemini ou OpenAI).
    Dependências:
        - os: Para manipulação de variáveis de ambiente.
        - langchain_google_genai: Para integração com o Google Gemini.
        - langchain_openai: Para integração com o OpenAI.
    Exemplo de uso:
        from llm import googleLLM, embbedLLM, llm
        google_model = googleLLM()
        embedding_model = embbedLLM(model='gemini')
        openai_model = llm(model='gpt')
"""
import os
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings


os.environ["GOOGLE_API_KEY"] = "AIzaSyA8DycW8OVImH9-UYp8QCVIPdK92gjVV28" #o certo é pegar de uma arquivo de ENV mas para uma demo não é necessária os.getenv('GEMINI_API_KEY')


OLLAMA_URL = os.getenv('OLLAMA_URL', 'host-gateway')

def getOllamaURL():
    """
    Função para retornar a URL do Ollama.
    Args:
        OLLAMA_URL (str): URL do Ollama. Padrão é 'localhost'.
    Returns:                
        str: URL do Ollama.
    """
    return OLLAMA_URL

def googleLLM():
    return ChatGoogleGenerativeAI(model="gemini-2.0-flash")


def embbedLLM(model = 'gemini'):
    """
    Função para retornar o modelo de embedding do Google Gemini.
    Args:
        model (str): O modelo a ser utilizado. Padrão é 'gemini'.
    Returns:                
        ChatGoogleGenerativeAI: O modelo de embedding do Google Gemini.
    """
    if model == 'gemini':
        return GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    
def llm(model = 'gemini'):
    return googleLLM()