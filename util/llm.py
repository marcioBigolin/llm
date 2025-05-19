"""
    Módulo para definir os modelos de LLM (Large Language Model) a serem utilizados.
    Este módulo contém funções para retornar instâncias de modelos LLM específicos,
    incluindo Google Gemini e OpenAI.
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
from langchain_openai import OpenAIEmbeddings, ChatOpenAI


os.environ["GOOGLE_API_KEY"] = os.getenv('GEMINI_API_KEY')
os.environ['OPENAI_API_KEY'] = os.getenv('API_KEY')

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

def gptLLM():
    """
    Função para retornar o modelo de LLM do OpenAI.
    Args:
        model (str): O modelo a ser utilizado. Padrão é 'gpt'.
    Returns:                
        ChatOpenAI: O modelo de LLM do OpenAI.
    """
    return ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

def embbedLLM(model = 'gemini'):
    """
    Função para retornar o modelo de embedding do Google Gemini.
    Args:
        model (str): O modelo a ser utilizado. Padrão é 'gemini'.
    Returns:                
        ChatGoogleGenerativeAI: O modelo de embedding do Google Gemini.
    """
    if model == 'gpt':
        return OpenAIEmbeddings()
    if model == 'gemini':
        return GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    
def llm(model = 'gemini'):
    if model == 'gpt':
        return gptLLM()
    if model == 'gemini':
        return googleLLM()