from flask import Flask

app = None
def create_app():
    global app
    if app is None:
        app = Flask(__name__)

        # from .controllers.rag import rag
        # from .controllers.pandas import pandas
        # from .controllers.geral import geral


        # app.register_blueprint(geral, url_prefix='/')
        # app.register_blueprint(rag, url_prefix='/rag')
        # app.register_blueprint(pandas, url_prefix='/pandas')


        
        # app.config['GATEWAY'] = os.getenv('GATEWAY')
        # app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 500  # 500MB
        # app.config['API_KEY'] = os.getenv('API_KEY')

    return app


