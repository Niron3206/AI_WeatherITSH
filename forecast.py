import tensorflow as tf
import pandas as pd

from visualization import future_weather

def forecast():
    model = tf.keras.models.load_model('saved_model/AI_WeatherITSH-2.0')

    df = pd.read_csv('./csv_files/moscow.csv')
    data = df[['pressure', 'tempC', 'humidity']]
    data.index = df['date_time']
    data = data.values

    data = data.reshape((1, 120, 3))
    
    #print(model.predict(data))
    steps = 6

    future_weather(model.predict(data), steps)
    
forecast()