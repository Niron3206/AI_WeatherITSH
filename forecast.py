import tensorflow as tf
import pandas as pd

from visualization import future_weather

def forecast():
    model = tf.keras.models.load_model('saved_model/AI_WeatherITSH', compile = True)

    df = pd.read_csv('./csv_files/moscow.csv')
    data = df[['pressure', 'tempC', 'humidity']]
    data.index = df['date_time']
    data = data.values

    data_mean = data.mean(axis=0)
    data_std = data.std(axis=0)
    data = (data-data_mean)/data_std

    data = data.reshape((1, 120, 3))

    prediction = model.predict(data, verbose=0)
    prediction = (prediction * data_std[1]) +  data_mean[1]

    steps = 6
    future_weather(prediction, steps)

forecast()