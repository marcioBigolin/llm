import os
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from langchain_qdrant import QdrantVectorStore


import util.llm as llm
import util.Eny as Eny


#Recupera ou define variaveis de ambiente
#TODO passar para o controlador
QDRANT = os.getenv("QDRANT_SERVER", 'qdrant')
QDRANT_PORT  = os.getenv("QDRANT_PORT", 6333)


#lista as variáveis de ambiente para debug
Eny.ds("Local: " + QDRANT)
Eny.ds(QDRANT_PORT)


#cria clients[collection] padrão
client = QdrantClient(host=QDRANT, port=QDRANT_PORT)



clients = {
    "interno": client,
}

#Estrutura de dados que representa o modelo do servidor para consulta 



#OLLAMA_URL = os.getenv('OLLAMA_URL')

def getClientModel(server, collection, model, criar=False):

    """
    Função para obter o cliente Qdrant apropriado com base no servidor, coleção e modelo fornecidos.
    Se a coleção não existir e criar for True, uma nova coleção será criada.
    
    Args:
        server (str): O servidor Qdrant a ser utilizado ('interno' ou 'externo').
        collection (str): O nome da coleção a ser utilizada.
        model (str): O modelo a ser utilizado ('gpt' ou 'gemini').
        criar (bool): Se True, cria uma nova coleção se ela não existir. Padrão é False.
    
    Returns:
        dict: Um dicionário contendo:
            - server (QdrantClient): O cliente Qdrant apropriado.
            - model (str): O modelo utilizado.
            - collection (str): O nome da coleção utilizada.
            - collectionName (str): O nome completo da coleção (incluindo o modelo).
    """
    # Verifica se o servidor é válido
    if server not in clients:
        raise ValueError(f"Servidor inválido: {server}. Use 'interno' ou 'externo'.")
    
    collectionName = collection + "_" + model

    # Verifica se a coleção existe
    collectionExists = clients[server].collection_exists(collectionName)
    
    # Se a coleção não existir e criar for True, cria uma nova coleção
    if not collectionExists and criar:
        clients[server].create_collection(collection_name=collectionName,  vectors_config=vetorDefinition(model)) #ver de criar no modelo correto
    elif not collectionExists:
        raise ValueError(f"A coleção '{collectionName}' não existe no servidor '{server}'.")
    
    return {
        'server': clients[server],
        'model': model,
        'collection': collection,
        'collectionName': collectionName,
        'chunkModel' : _defineChunks(model)
    }


def getVectorStore(serverModel):
    return QdrantVectorStore(
            client=serverModel['server'],
            collection_name=serverModel['collectionName'],
            embedding=llm.embbedLLM(model=serverModel['model']),
        )

def getRetriever(serverModel):
    """
    Função para obter o cliente Qdrant apropriado com base no servidor, coleção e modelo fornecidos.
    Se a coleção não existir e criar for True, uma nova coleção será criada.
    
    Args:
           serverModel (dict): Um dicionário contendo as informações do servidor, coleção e modelo.
                - server (str): O servidor Qdrant a ser utilizado ('interno' ou 'externo').
                - collection (str): O nome da coleção a ser utilizada.
                - model (str): O modelo a ser utilizado ('gpt' ou 'gemini').    
    Returns:
        dict: Um dicionário contendo:
            - server (QdrantClient): O cliente Qdrant apropriado.
            - model (str): O modelo utilizado.
            - collection (str): O nome da coleção utilizada.
            - collectionName (str): O nome completo da coleção (incluindo o modelo).
    """

    vectorstore = QdrantVectorStore(
            client=serverModel['server'],
            collection_name=serverModel['collectionName'],
            embedding=llm.embbedLLM(model=serverModel['model']),
        )

    retriever=vectorstore.as_retriever(        
                search_type="similarity_score_threshold",
                search_kwargs={'score_threshold': 0.5})

    
    return retriever

def vetorDefinition(model): 
    """
    Função para definir a estrutura do vetor com base no modelo fornecido.
    
    Args:
        model (str): O modelo a ser utilizado ('gpt', 'gemini'...).
    
    Returns:
        dict: Um dicionário contendo a definição do vetor.
    """
    if model == 'gpt':
        return VectorParams(   
            size=1536,
            distance=Distance.COSINE
        )
    elif model == 'gemini':
        return VectorParams(   
            size=768,
            distance=Distance.COSINE
        )
    else:
        raise ValueError(f"Modelo inválido: {model}. Use 'gpt' ou 'gemini' ou 'ollama'.")
   
def colectionCreate(server, collectionName, vectorSize = 1024, vectorDistance = Distance.COSINE):
    """
    Função para criar uma coleção no servidor Qdrant.
    
    Args:
        server (str): O servidor Qdrant a ser utilizado ('interno' ou 'externo').
        collectionName (str): O nome da coleção a ser criada.
        vectorSize (str): O modelo a ser utilizado ('gpt', 'gemini'...).
    
    Returns:
        bool: True se a coleção foi criada com sucesso, False caso contrário.
    """
    # Verifica se o servidor é válido
    if server not in clients:
        raise ValueError(f"Servidor inválido: {server}. Use 'interno' ou 'externo'.")
    

    # Cria a coleção
    clients[server].create_collection(collection_name=collectionName,  vectors_config=VectorParams(   
            size=vectorSize,
            distance=vectorDistance
        ))
    
    return True


def _defineChunks(model):
    base = {
        'gpt' : { 'size': 1000, 'overlap': 200},
        'gemini' : { 'size': 500, 'overlap': 200}
    }

    return base[model]