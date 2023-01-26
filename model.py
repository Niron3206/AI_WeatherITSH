import tensorflow as tf

import matplotlib as mpl
import os
import pandas as pd

from intervals_organization import organize

mpl.rcParams['figure.figsize'] = (8, 6)
mpl.rcParams['axes.grid'] = False

# setting global random seed
tf.random.set_seed(13)

# strings for training (300000 - default)
TRAIN_SPLIT = 400000

# cycles to go through (10 - default)
EPOCHS = 10

# steps in one cycle (500 - default)
EVALUATION_INTERVAL = 1000

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
    STEP = 6                                    # 1 step = 10 min, so if you set it to 6, it will only take data in every hour
    past_history = 720                          # past_history - amount of choosen data for prediction (5days * 24hours * 6steps = 750)
    future_target = 72                          # future_target - how far in time to predict (12hours * 6steps = 72)


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
    model.add(tf.keras.layers.Dense(72))
    model.compile(optimizer=tf.keras.optimizers.RMSprop(clipvalue=1.0), loss='mae')

    # learning model
    model.fit(train, epochs=EPOCHS,
                steps_per_epoch=EVALUATION_INTERVAL,
                validation_data=val, validation_steps=50)

    '''
    for x, y in val.take(3):
        multi_step_plot(x[0], y[0], model.predict(x)[0], STEP)
    '''
    
    model.save('saved_model/AI_WeatherITSH-2.0')

model()