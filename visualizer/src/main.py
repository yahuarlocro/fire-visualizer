"""Web application initializer
"""
from visualizer import app

if __name__ == "__main__":
    # app.run()
    # app.run(host='0.0.0.0', port=8001,load_dotenv='.flaskenv')
    app.run(load_dotenv='.flaskenv')