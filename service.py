import os
from src import create_app


app = create_app()

if __name__ == '__main__':

    print("LLM iniciado [DEV MODE]")
    app.run(debug=True, passthrough_errors=True,
                use_debugger=False, use_reloader=True, 
                host='0.0.0.0', port=4509)