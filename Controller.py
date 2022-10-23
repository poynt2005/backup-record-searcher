from flask import Flask, request, jsonify, send_file, redirect
from  urllib.parse import unquote, quote
from flask_cors import CORS
from datetime import datetime, timezone
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

        search_rst_arr = model.search_target_commics(file_name)

        return_data_arr = []

        for search_rst in search_rst_arr:
            update_date = datetime.fromisoformat(search_rst[2])
            info_json = None
            try:
                info_json = json.loads(search_rst[7])
            except:
                info_json = None
            return_data = {
                'comic_id': search_rst[0],
                'drive_name': search_rst[1],
                'update_utc_isostr': update_date.isoformat() + 'Z',
                'size_in_bytes': search_rst[3],    
                'is_folder': not not search_rst[4],
                'comic_name': search_rst[5],
                'pic_count': search_rst[6],
                'info_json': info_json
            }
            return_data_arr.append(return_data)

        return jsonify({ 'method': 'POST', 'path': 'search', 'message': return_data_arr }), 200

        