import urllib.request
import urllib.parse
import urllib.error
import json
import hashlib

def login(api_key, md5_app_id, login, password):
    
    data = {
        'cmd': 'userLogon',
        'uuid': md5_app_id,
        'api_key': api_key,
        'lang': 'ru',
        'login': login,
        'hash': hashlib.md5((md5_app_id + hashlib.md5(password.encode('utf-8')).hexdigest()).encode('utf-8')).hexdigest()
    }

    try:
        request = urllib.request.Request('http://narodmon.ru/api', json.dumps(data).encode('utf-8'))
        response = urllib.request.urlopen(request)
        result = json.loads(response.read())

        print(result)

    except urllib.error.URLError as e:
        print('HTTP error:', e)

    except (ValueError, TypeError) as e:
        print('JSON error:', e)