import os, sys, json, math
from urllib import request

script_name = sys.argv[0].split(os.sep)[-1]
server_name = None

def check_server():
        try:
            res = request.urlopen('http://%s/check_server' % server_name)
            return res.read().decode('utf-8').strip() == 'server_listening'
        except:
            return False


if os.path.isfile('.recorder_server'):
    with open('.recorder_server', 'r', encoding='utf-8') as f:
        server_name = f.read().strip()
        if not check_server():
            print('Server %s not available, please re-enter the server' % server_name)
            server_name = None

if server_name is None:
    server_name = input('Input your server name: ')

    if not check_server():
        print('Server %s not available' % server_name)
        exit(1)

    with open('.recorder_server', 'w', encoding='utf-8') as f:
        f.write(server_name)

list_dict = []
to_store = []

for i in os.listdir(b'.'):
    n = ''
    try:
        n = i.decode('utf-8')
    except:
        n = i.decode('utf-8', 'replace')

    if n == '.recorder_server' or n == script_name:
        continue
    if not n in list_dict:
        list_dict.append(n)

        to_store.append({
            'name': n,
            'date': math.floor(os.path.getmtime(i)*1000),
            'size': os.path.getsize(i) // 1024,
            'isFolder': os.path.isdir(i)
        })

to_store_binary = json.dumps(to_store, ensure_ascii=False).encode('utf-8')

try:
    req = request.Request('http://%s/add_comic' % server_name, data=to_store_binary)
    res = request.urlopen(req)
    result_json = json.loads(res.read())
    print('Stored: %d books' % result_json['stored'])
    print('Books: [%s] duplicated, not saved' % ', '.join(result_json['duplicated']))
except:
    print('Save content failed')

input('Process end, Press Enter to exit...')
