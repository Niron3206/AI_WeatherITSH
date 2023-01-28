import matplotlib.pyplot as plt
import numpy as np

def create_time_steps(length):
    return list(range(-length, 0))

def multi_step_plot(history, true_future, prediction, STEP):
    plt.figure(figsize=(12, 6))
    num_in = create_time_steps(len(history))
    num_out = len(true_future)

    plt.plot(num_in, np.array(history[:, 1]), label='History')
    plt.plot(np.arange(num_out)/STEP, np.array(true_future), 'bo',
            label='True Future')
    if prediction.any():
        plt.plot(np.arange(num_out)/STEP, np.array(prediction), 'ro',
                label='Predicted Future')
    plt.legend(loc='upper left')
    plt.show()

def future_weather(prediction, STEP):

    plt.figure(figsize=(12, 6))
    plt.xlabel('Next Hours')
    plt.ylabel('Temperature (°C)')

    for i, x in enumerate(prediction.T):
        plt.plot(i/STEP, x, 'bo')

    plt.legend(loc='upper left')
    plt.show()