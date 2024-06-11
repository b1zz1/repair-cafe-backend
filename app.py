from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/user/*": {"origins": "http://localhost:3000"}})

@app.route('/')
@app.route('/home')
def index():
    return "Sim"


@app.route('/user/create', methods=['GET', 'POST'])
def userCreate():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    return {}


@app.route('/user/read', methods=['GET'])
def userRead():
    return 0


@app.route('/user/update', methods=['GET', 'PUT']) # Verificar a viabilidade de PUT ou PATCH
def userUpdate():
    return 0


@app.route('/user/delete', methods = ['GET'])
def userDelete():
    return 0


if __name__ == '__main__':
    app.run(debug=True)
