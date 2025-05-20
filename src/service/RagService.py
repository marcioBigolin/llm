import io

import util.QdrantServer as QdrantServer
import util.Eny as Eny
from PyPDF2 import PdfReader


def treinarArquivo(arquivo):
    """
    Função para treinar o arquivo.
    """
    # Lógica para treinar o arquivo
    serverModel = QdrantServer.getClientModel('interno', 'demo', 'gemini', criar=True) #Conecta e cria a coleção
      

    vectorstore = QdrantServer.getVectorStore(serverModel) #define o vetorstore

    metadata = {
        'source': arquivo,
        'pagina': 1,

    }

    all_text = []
    all_contextos = []
    Eny.ds(metadata)
    try:
        file = open(arquivo, 'rb')
        pdfReader = PdfReader(io.BytesIO(file.read()))
    except Exception as e:
        Eny.ds("Error: Unable to read the PDF file. It may be corrupted.")

    for page_num in range(len(pdfReader.pages)):

        page = pdfReader.pages[page_num]
        text = page.extract_text()

        #se processsar imagens for true, processa as imagens do PDF
        # if images:
        #     processedImages = ImageServices.processaImages(page.images) #o ideal é um banco de descrições e não concatenar para o próximo bolsista
        #     for image in processedImages:
        #         Eny.ds("Imagem: " + str(image))   
        #         text += " <IMAGEM>" + image["descricao"] + "</IMAGEM> " 
        #     metadata['images'] = processedImages
        
        texts = get_chunksV2(text, serverModel['chunkModel']['size'], serverModel['chunkModel']['overlap'])
        contextos = contexts(texts, page_num, metadata)

        all_text.extend(texts)
        all_contextos.extend(contextos)

    vectorstore.add_texts(all_text, all_contextos)


def get_chunksV2(text, chunk_size=1000, chunk_overlap=200):
    from langchain.text_splitter import RecursiveCharacterTextSplitter

    # Configura o RecursiveCharacterTextSplitter com os separadores desejados
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n", "."],  # Quebra por \n e .
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def contexts(texts, page_num, metadata):
    contextos = []
    newContext = metadata.copy()
    for texto in texts:
        newContext['pagina'] = page_num+1
        contextos.append(newContext)
    return contextos
