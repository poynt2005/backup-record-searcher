from flask import Flask, request, jsonify, send_file, redirect
from  urllib.parse import unquote, quote
from flask_cors import CORS
import os, json

app = Flask(__name__)
CORS(app)

'''
store_file = []
{name: 'xxx', date: 'timestamp', size: 'xx(byte)', isFolder: Boolean}
'''

if not os.path.isfile(os.path.join('/data', 'store.json')):
    with open(os.path.join('/data', 'store.json'), 'w', encoding='utf-8') as f:
        f.write('[]')

@app.route('/', methods=['GET'])
def root_route():
    if request.method == 'GET':
        return 'Hello message from ComicRecorder', 200

@app.route('/check_server', methods=['GET'])
def check_server():
    if request.method == 'GET':
        return 'server_listening', 200

@app.route('/add_comic', methods=['POST'])
def add_comic():
    if request.method == 'POST':
        content = json.loads(request.get_data().decode('utf-8'))

        store_file = []
        with open(os.path.join('/data', 'store.json'), 'r', encoding='utf-8') as f:
            store_file = json.loads(f.read())

        all_keys = []
        if len(store_file):
            all_keys = [k['name'] for k in store_file]

        duplicated = []
        stored_count = 0

        for k in content:
            if not k['name'] in all_keys:
                stored_count += 1
                store_file.append(k)
            else:
                duplicated.append(k['name'])
        
        with open(os.path.join('/data', 'store.json'), 'w', encoding='utf-8') as f:
            f.write(json.dumps(store_file, ensure_ascii=False))
        
        store_file = None
        
        return jsonify({'stored': stored_count, 'duplicated': duplicated}), 200

@app.route('/search',  methods=['POST'])
def search():
    if request.method == 'POST':
        body = request.get_json()
        file_name = unquote(body['file_name'])

        search_rst = []

        store_file = []
        with open(os.path.join('/data', 'store.json'), 'r', encoding='utf-8') as f:
            store_file = json.loads(f.read())
        
        store_file_name = [store_file[i]['name'] for i in range(len(store_file))]

        for i in range(len(store_file_name)):
            f = store_file_name[i]
            if file_name.lower() in f.lower():
                search_rst.append({
                    'name': quote(f),
                    'date': store_file[i]['date'],
                    'size': store_file[i]['size'],
                    'isFolder': store_file[i]['isFolder']
                })

        return jsonify({ 'method': 'POST', 'path': 'search', 'message': search_rst })

if __name__ == '__main__':
    app.run(port=8586,host='0.0.0.0',debug=True)

