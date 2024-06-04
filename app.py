from flask import Flask

from database.db import *

app = Flask(__name__)


@app.route('/')
def index():
    return 0


@app.route('/user/create', methods = ['GET', 'POST'])
def userCreate():
    return 0


@app.route('/user/read', methods = ['GET'])
def userRead():
    return 0


@app.route('/user/update', methods = ['GET', 'PUT']) # Verificar a viabilidade de PUT ou PATCH
def userUpdate():
    return 0


@app.route('/user/delete', methods = ['GET'])
def userDelete():
    return 0