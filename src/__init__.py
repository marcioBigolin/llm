from flask import Flask
from flask_cors import CORS

app = None
def create_app():
    global app
    if app is None:
        app = Flask(__name__)
        CORS(app) # This will enable CORS for all routes

        from .controllers.RagController import rag
        from .controllers.ChatController import chat


        app.register_blueprint(chat, url_prefix='/')
        app.register_blueprint(rag, url_prefix='/rag')


        

    return app


