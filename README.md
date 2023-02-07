
![AI_WeatherITSH](https://media.discordapp.net/attachments/695563421491396728/1069339477945897163/AI_WeatherITSH.png)

**English** | [Русский](./README-ru.md)

# 🌥️ AI_WeatherITSH

**AI_WeatherITSH** - my school project that forecasts future weather by using [neural networks](https://www.ibm.com/topics/neural-networks) and predicting temperature for given intervals. It also represents one of the most popular solution for [time series forecasting](https://en.wikipedia.org/wiki/Time_series) problems (weather forecast in my case).

My model is made of [Recurrent Neural Networks](https://en.wikipedia.org/wiki/Recurrent_neural_network) (RNN), to be more precise one of its variation - [Long short-term memory](https://en.wikipedia.org/wiki/Long_short-term_memory) (LSTM).

The main goal of project is to research and learn something new about Neural Networks and how they work.

## ⚠️ Project in development

It has bugs... and there's lot of things to improve.

## 🔧 Downloading and setting up

1. Make sure you have version of python `3.10.X` or higher.
2. Set up your environment (venv/conda etc... by your choice) and install all requirements.
3. Compile and train the model by simply running `model.py` script. (You can adjust model as you want, merely edit every needed variables)

Done... you've got a trained and fully capable of predicting model.

#### So how do we predict?

In this project, I used REST API from `https://narodmon.ru` site. To obtain the weather data, you have to set up some environment variables in `narodmonitoring\.env` file.
Before you do that, you must create an account there and get your api key, login and password.
Also, find any public sensors(pressure, temperature, humidity) then get their ids and insert into `history.py` script.
Run `__init__.py`.

After when everything is done, run `forecast.py` script to get your forecast as matplot visualization.

## 📷 Screenshots

Weather forecast from 10:00 to 22:00 in 24.07.2022 (Moscow)

![10.00-22.00_24.07.22](https://media.discordapp.net/attachments/695563421491396728/1069341219391549460/10.00-22.00_24.07.22.png)

Weather forecast from 0:00 to 12:00 in 28.01.2023 (Moscow) (not so accurate temperature, depends on time of training model)

![0.00-12.00_28.01.23](https://media.discordapp.net/attachments/695563421491396728/1069394784529170442/0.00-12.00_28.01.23.png)
