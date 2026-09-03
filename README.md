![AI_WeatherITSH](https://github.com/Niron3206/AI_WeatherITSH/raw/master/AI_WeatherITSH.png)

**English** | [Русский](./README-ru.md)

# 🌥️ AI_WeatherITSH

The model predicts air temperature a day ahead from a history of observations. An LSTM network takes seven days of hourly readings (pressure, temperature and a third channel) and returns 144 temperature values: one for every ten minutes of the next 24 hours.

The network was trained on the public Jena Climate 2009–2016 dataset. Forecasts are built from readings of amateur weather sensors, served by the narodmon.ru REST API.

The project was written in 2023 to find out how recurrent networks behave on time series. A study exercise, not a weather forecasting service. It has not been updated since.

## Data

**Training.** Jena Climate 2009–2016, recordings of the weather station at the Max Planck Institute for Biogeochemistry in Jena, Germany: 420,551 records at a 10-minute interval, 14 meteorological variables. `model.py` downloads the archive from TensorFlow storage on its own. Three of the 14 columns went into the model: `p (mbar)`, `T (degC)` and `rho (g/m**3)`. The first 300,000 records go to training, the remainder to validation. All three columns are brought to zero mean and unit variance using the statistics of the training part.

**Splitting the series into intervals.** `intervals_organization.py` moves a window along the series one record per step. At each position it takes the previous 1008 records (exactly 7 days) and thins them with a step of 6, which leaves 168 hourly points of 3 features. What the network learns to guess is the next 144 temperature values, that is, a day ahead at the original ten-minute resolution.

**Forecasting.** The `narodmonitoring` package logs into the narodmon.ru API (`userLogon`) and requests a month of history (`sensorsHistory`) for the three sensor ids from `.env`: pressure, temperature, humidity. All of it lands in `csv_files/history_1month.csv`, and the last 168 rows go separately into `csv_files/history_7days.csv`, which is what reaches the model. `forecast.py` standardizes that window by its own mean and deviation, reshapes it to `(1, 168, 3)`, runs it through the network and converts the result back to degrees using the temperature statistics of the same window.

## Model

A sequential Keras model:

| Layer | Parameters |
| --- | --- |
| LSTM | 32 units, `return_sequences=True`, input shape `(168, 3)` |
| LSTM | 16 units, `activation='relu'` |
| Dense | 144 outputs, one per ten-minute step of the horizon |

Optimizer RMSprop with `clipvalue=1.0`, loss function: mean absolute error. Training runs for 10 epochs of 200 steps, batch 256, shuffle buffer 10,000, 50 validation steps per epoch. The random seed is fixed at 13. The finished model is saved in SavedModel format to `saved_model/AI_WeatherITSH-24H`. TensorFlow 2.11.1, Python 3.10.

## Limitations

The network was trained on one set of data and is applied to another. Training runs on a research weather station in Jena, forecasting on amateur sensors in Moscow and the surrounding region. The third input feature does not match either: air density during training, humidity during forecasting. Whether the model survives that move was never checked.

There are no quality figures here. Only the loss function was tracked during training.

Two more things hurt accuracy at inference. Normalization is computed from the statistics of the input window itself instead of the ones saved from training, so the same weather is scaled differently depending on the week. And the histories of the three sensors are joined by row number, with no time alignment and no handling of gaps; if the API is unavailable, the script stops.

Today it would be worth doing this differently: keep one feature set for training and forecasting, save the scaler together with the model, measure MAE on a held-out period against a baseline, and train the network on data from the same sensors the forecast is later built from.

## 🔧 Downloading and setting up

1. Make sure you have version of python `3.10.X` or higher.
2. Set up your environment (venv/conda etc... by your choice) and install all requirements.
3. Compile and train the model by simply running `model.py` script. (You can adjust model as you want, merely edit every needed variables)

Done... you've got a trained and fully capable of predicting model.

#### So how do we predict?

The project uses the REST API from `https://narodmon.ru` site. To obtain the weather data, you have to set up some environment variables in `narodmonitoring\.env` file.
Before you do that, you must create an account there and get your api key, login and password.
Also, find any public sensors (pressure, temperature, humidity) then get their ids and insert into `narodmonitoring\.env` file.
Run `__init__.py`.

After when everything is done, run `forecast.py` script to get your forecast as matplot visualization.

## 📷 Screenshots

The screenshots were taken with an earlier version of the model, its horizon was 12 hours.

Weather forecast from 10:00 to 22:00 in 24.07.2022 (Moscow)

![10.00-22.00_24.07.22](https://github.com/Niron3206/AI_WeatherITSH/raw/master/10.00-22.00_24.07.22.png)

Weather forecast from 0:00 to 12:00 in 28.01.2023 (Moscow) (not so accurate temperature, depends on time of training model)

![0.00-12.00_28.01.23](https://github.com/Niron3206/AI_WeatherITSH/raw/master/0.00-12.00_28.01.23.png)

## License

MIT, see [LICENSE.md](./LICENSE.md).
