from flask import Flask, request, jsonify, send_file, redirect
from  urllib.parse import unquote, quote
from flask_cors import CORS
import os, json

class Controller:
    def __init__(self):
        pass

    def home(self):
        return 'Hello message from ComicRecorder', 200

    def check(self):
        return 'server_listening', 200
    
    #from python  client
    def add_comic(self, model):
        contents = json.loads(request.get_data().decode('utf-8'))

        return_data = {
            'stored': 0, 
            'duplicated': [],
            'updated': []
        }
        
        for content in contents:
            rst = model.get_single_commic(content['name'])

            if not len(rst) == 0:
                comic_id = int(rst[0][0])

                if not len(content['info']) == 0:
                    model.update_info({'id': comic_id, 'info': content['info']})
                    return_data['updated'].append(content['name'])
                else:
                    
                    return_data['duplicated'].append(content['name'])
            else:
                model.insert_comic({
                    'drive': content['drive'],
                    'timestamp': content['timestamp'],
                    'size': content['size'],
                    'isFolder': 1 if content['isFolder'] else 0,
                    'name': content['name'],
                    'info': None if len(content['info']) == 0 else content['info'],
                    'picCount': content['picCount']

                })

                return_data['stored'] = return_data['stored'] + 1
        
        return jsonify(return_data), 200

    def search(self, model):
        body = request.get_json()
        file_name = unquote(body['file_name'])

        search_rst = model.search_target_commics(file_name)

        return jsonify({ 'method': 'POST', 'path': 'search', 'message': search_rst }), 200

        