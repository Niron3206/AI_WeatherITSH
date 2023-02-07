import urllib.request
import urllib.parse
import urllib.error
import json
import pandas as pd
from datetime import datetime

def get_history(api_key, md5_app_id):

    pressure_id = 'your id here'
    temperature_id = 'your id here'
    humidity_id = 'your id here'
    period = 'month'
    offset = '1'

    pressure = {
        'cmd': 'sensorsHistory',
        'uuid': md5_app_id,
        'api_key': api_key,
        'lang': 'ru',
        'id': pressure_id,
        'period': period,
        'offset ': offset
    }
    temperature = {
        'cmd': 'sensorsHistory',
        'uuid': md5_app_id,
        'api_key': api_key,
        'lang': 'ru',
        'id': temperature_id,
        'period': period,
        'offset ': offset
    }
    humidity = {
        'cmd': 'sensorsHistory',
        'uuid': md5_app_id,
        'api_key': api_key,
        'lang': 'ru',
        'id': humidity_id,
        'period': period,
        'offset ': offset
    }

    try:
        pressure_result = json.loads(urllib.request.urlopen(
                                    urllib.request.Request('http://narodmon.ru/api',
                                                            json.dumps(pressure).encode('utf-8'))).read())
        temperature_result = json.loads(urllib.request.urlopen(
                                    urllib.request.Request('http://narodmon.ru/api',
                                                            json.dumps(temperature).encode('utf-8'))).read())
        humidity_result = json.loads(urllib.request.urlopen(
                                    urllib.request.Request('http://narodmon.ru/api',
                                                            json.dumps(humidity).encode('utf-8'))).read())
    
        pressure_result = pressure_result['data']
        temperature_result = temperature_result['data']
        humidity_result = humidity_result['data']

        l = []
        i = 0
        while i < len(pressure_result):
            l.append({'time': pressure_result[i]['time'],
                        'pressure': pressure_result[i]['value'],
                        'temperature': temperature_result[i]['value'],
                        'humidity': humidity_result[i]['value']})
            i += 1
        df = pd.DataFrame(l)

        for i in df['time']:
            df = df.replace(i, datetime.utcfromtimestamp(i).strftime('%d-%m-%Y %H:%M:%S'))
        
        df.to_csv('csv_files/history_1month.csv', encoding='utf-8', index=False)

        df = df[len(df) - 168:]
        df.to_csv('csv_files/history_7days.csv', encoding='utf-8', index=False)

    except urllib.error.URLError as e:
        print('HTTP error:', e)

    except (ValueError, TypeError) as e:
        print('JSON error:', e)