from flask import Flask, request, jsonify, send_file, redirect
from  urllib.parse import unquote, quote
from flask_cors import CORS
import os, json

from Model import Model
from Controller import Controller

app = Flask(__name__)
CORS(app)

model = Model(os.path.join(os.getcwd(), 'datenbank', 'datenbank.db'))
controller = Controller()


@app.route('/', methods=['GET'])
def root_route():
    if request.method == 'GET':
        return controller.home()

@app.route('/check_server', methods=['GET'])
def check_server():
    if request.method == 'GET':
        return controller.check()

@app.route('/add_comic', methods=['POST'])
def add_comic():
    if request.method == 'POST':
        return controller.add_comic(model)

@app.route('/search',  methods=['POST'])
def search():
    if request.method == 'POST':
        return controller.search(model)

if __name__ == '__main__':
    app.run(port=8586,host='0.0.0.0',debug=True)