import matplotlib.pyplot as plt

def future_weather(prediction, STEP):

    plt.figure(figsize=(12, 6))
    plt.xlabel('Next Hours')
    plt.ylabel('Temperature (°C)')

    for i, x in enumerate(prediction.T, start=1):
        plt.plot(i/STEP, x, 'bo')

    plt.legend(loc='upper left')
    plt.show()