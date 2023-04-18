import hashlib
import uuid
import os
if not os.path.exists('csv_files'):
    os.makedirs('csv_files')

from login import login
from history import get_history

from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('API_KEY')
_login = os.getenv('LOGIN')
password = os.getenv('PASSWORD')

pressure_id = os.getenv('pressure_id')
temperature_id = os.getenv('temperature_id')
humidity_id = os.getenv('humidity_id')

app_id = str(uuid.getnode()).encode('utf-8')
md5_app_id = hashlib.md5(app_id).hexdigest()
    
login(api_key, md5_app_id, _login, password)
get_history(api_key, md5_app_id, pressure_id, temperature_id, humidity_id)