## Pequeno grande tutorial para o MiniLLM desenvolvido aqui

Blueprints são uma excelente maneira (gambiara) de estruturar e organizar uma aplicação Flask. Aqui está um esboço da organização de uma aplicação Flask com Blueprints:

```
llm/
├── src/
│   ├── __init__.py
│   ├── controllers/
│   │   ├── __init__.py
│   │   ├── rag_controller.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── rag.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── rag_service.py
│   ├── config.py
├── service.py
```

### Detalhes dos Arquivos

#### `service.py`
Este será o ponto de entrada para a sua aplicação. Inicia a aplicação flask.

```python
# service.py
from src import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
```

#### `src/__init__.py`
Aqui, você cria a aplicação Flask e registra os Blueprints.

```python
# llm_service/__init__.py
from flask import Flask
from .models import db
from .controllers.chat_controller import chat_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('llm_service.config.Config')

    # Initialize the database
    db.init_app(app)

    # Register Blueprints
    app.register_blueprint(chat_bp, url_prefix='/chat')

    return app
```

#### `llm_service/models/chat.py`
Definição do modelo `Sessao`.

```python
# llm_service/models/chat.py
from . import db
from sqlalchemy import Column, Integer, String, DateTime, func

class Sessao(db.Model):
    __tablename__ = 'chat'
    __table_args__ = {"schema": "llm"}

    id = Column(Integer, primary_key=True)
    usuario_email = Column(String)
    user_agent = Column(String)
    data_inicio = Column(DateTime, default=func.now())
```

#### `llm_service/controllers/__init__.py`
Inicialização do pacote de controladores (pode estar vazio).

```python
# llm_service/controllers/__init__.py
```

#### `llm_service/controllers/chat_controller.py`
Controlador usando Blueprint. Os endpoints de controle de chat são gerenciados aqui.


```python
# llm_service/controllers/chat_controller.py
from flask import Blueprint, request, jsonify
from llm_service.models import db, Sessao

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/', methods=['GET'])
def get_chat():
    sessoes = Sessao.query.all()
    return jsonify([{"id": chat.id, "usuario_email": chat.usuario_email, "user_agent": chat.user_agent, "data_inicio": chat.data_inicio} for chat in sessoes])

@chat_bp.route('/', methods=['POST'])
def create_chat():
    data = request.get_json()
    nova_chat = Sessao(
        usuario_email=data.get("usuario_email"),
        user_agent=data.get("user_agent")
    )
    db.session.add(nova_chat)
    db.session.commit()
    return jsonify({"message": "Sessão criada com sucesso!"}), 201
```

#### `llm_service/services/__init__.py`
Inicialização do pacote de serviços (pode estar vazio).

```python
# llm_service/services/__init__.py
```

#### `llm_service/services/sessao_service.py`
Serviços relacionados à `Sessao`.

```python
# llm_service/services/sessao_service.py
from llm_service.models import db, CHat

def criar_sessao(usuario_email, user_agent):
    nova_sessao = Sessao(usuario_email=usuario_email, user_agent=user_agent)
    db.session.add(nova_sessao)
    db.session.commit()
    return nova_sessao
```

### Conclusão

Neste exemplo, utilizamos Flask Blueprints para separar cada controlador em seu próprio módulo, melhorando assim a organização e a manutenibilidade do código. Além disso, temos arquivos dedicados para modelos, serviços e configuração, o que ajuda a isolar responsabilidades e facilita o crescimento da aplicação.




#### `llm_service/services/sessao_service.py`
Lógica de negócios e interações complexas com a base de dados são gerenciadas aqui.

```python
# llm_service/services/sessao_service.py
from llm_service.models import db, Sessao

def criar_sessao(usuario_email, user_agent):
    nova_sessao = Sessao(usuario_email=usuario_email, user_agent=user_agent)
    db.session.add(nova_sessao)
    db.session.commit()
    return nova_sessao
```

### Vantagens desta Estrutura:

1. **Separação de Responsabilidades**:
   - **Modelos**: Contêm a definição da estrutura de dados.
   - **Serviços**: Contêm a lógica de negócios e interações complexas com a base de dados.
   - **Controladores**: Gerenciam as solicitações HTTP e coordenam entre o cliente e os serviços.

2. **Escalabilidade**:
   - Facilita o acréscimo de novos endpoints, modelos e serviços sem tornar o código confuso.

3. **Manutenibilidade**:
   - Código modular é mais fácil de testar, debugar e manter.

### Expansão da Estrutura:

Para continuar organizando sua aplicação, considere os seguintes passos conforme a necessidade:

1. **Novos Módulos**:
   - Adicione novos Blueprints em `controllers` conforme novas funcionalidades são adicionadas (`user_controller.py`, `product_controller.py`, etc.)

2. **Serviços Compartilhados**:
   - Adicione serviços comuns a `services` (`mail_service.py`, `auth_service.py`, etc.)

3. **Configurações Específicas**:
   - Use diferentes arquivos de configuração (`config_dev.py`, `config_prod.py`) que podem ser carregados dependendo do ambiente.

4. **Middlewares e Extensões**:
   - Adicione middlewares para autenticação, logging, etc., no `__init__.py` principal do pacote `llm_service`.
