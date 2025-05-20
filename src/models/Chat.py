from datetime import datetime


class Chat:
  
    query = ''
    response = ''
    dataPergunta = datetime.now()
    dataResposta = None

    referencias = []


    def to_dict(self):
        return {
            'id': self.id,
            'response': self.response,
            'type': self.type,
            'codigo': self.codigo
        }
    
