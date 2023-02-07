import tensorflow as tf

import os
import pandas as pd

from intervals_organization import organize

# setting global random seed
tf.random.set_seed(13)

# strings for training (300000 - default)
TRAIN_SPLIT = 300000

# cycles to go through (10 - default)
EPOCHS = 10

# steps in one cycle (200 - default)
EVALUATION_INTERVAL = 200

def model():

    # loading data
    zip_path = tf.keras.utils.get_file(
        origin='https://storage.googleapis.com/tensorflow/tf-keras-datasets/jena_climate_2009_2016.csv.zip',
        fname='jena_climate_2009_2016.csv.zip',
        extract=True)
    csv_path, _ = os.path.splitext(zip_path)
    df = pd.read_csv(csv_path)

    # taking tempreture
    dataset = df[['p (mbar)', 'T (degC)', 'rho (g/m**3)']]
    dataset.index = df['Date Time']
    dataset = dataset.values

    # standardization (normalization)
    data_mean = dataset[:TRAIN_SPLIT].mean(axis=0)
    data_std = dataset[:TRAIN_SPLIT].std(axis=0)
    dataset = (dataset-data_mean)/data_std

    # separation for trainings
    STEP = 6                                     # 1 step = 10 min, so if you set it to 6, it will only take data in every hour
    past_history = 1008                          # past_history - amount of choosen data for prediction (7days * 24hours * 6steps = 1008)
    future_target = 144                          # future_target - how far in time to predict (24hours * 6steps = 144)


    x_train, y_train = organize(dataset, dataset[:,1], 0, TRAIN_SPLIT, past_history, future_target, STEP)

    x_val, y_val = organize(dataset, dataset[:,1], TRAIN_SPLIT, None, past_history, future_target, STEP)


    # shuffling, batching and caching dataset
    BATCH_SIZE = 256
    BUFFER_SIZE = 10000

    train = tf.data.Dataset.from_tensor_slices((x_train, y_train))
    train = train.cache().shuffle(BUFFER_SIZE).batch(BATCH_SIZE).repeat()
    
    val = tf.data.Dataset.from_tensor_slices((x_val, y_val))
    val = val.batch(BATCH_SIZE)

    # compiling and running lstm model
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.LSTM(32,
                                    return_sequences=True,
                                    input_shape=x_train.shape[-2:]))
    model.add(tf.keras.layers.LSTM(16, activation='relu'))
    model.add(tf.keras.layers.Dense(future_target))
    model.compile(optimizer=tf.keras.optimizers.RMSprop(clipvalue=1.0), loss='mae')

    # learning model
    model.fit(train, epochs=EPOCHS,
                steps_per_epoch=EVALUATION_INTERVAL,
                validation_data=val, validation_steps=50)

    if not os.path.exists('saved_model'):
        os.makedirs('saved_model')
        
    model.save('saved_model/AI_WeatherITSH-24H')

model()