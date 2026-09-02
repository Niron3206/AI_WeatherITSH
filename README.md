![AI_WeatherITSH](https://github.com/Niron3206/AI_WeatherITSH/raw/master/AI_WeatherITSH.png)

**English** | [Русский](./README-ru.md)

# 🌥️ AI_WeatherITSH

Short-term temperature forecasting treated as a time series problem. An LSTM network takes a seven-day window of hourly weather observations (pressure, temperature and a third channel) and predicts air temperature for the next 24 hours at a 10-minute resolution. The network is trained on the public Jena Climate 2009–2016 dataset and then applied to readings from public amateur weather sensors obtained through the `narodmon.ru` REST API.

The project was written in 2023 as a study of recurrent networks and their application to time series. It is a learning exercise, not a production forecasting service, and it is no longer maintained.

## Data

**Training.** Jena Climate 2009–2016, recorded at the Max Planck Institute for Biogeochemistry in Jena, Germany: 420 551 records at a 10-minute interval, 14 meteorological variables. The dataset is downloaded automatically by `model.py` from the TensorFlow storage. Three columns are used: `p (mbar)`, `T (degC)` and `rho (g/m**3)`. The first 300 000 records form the training split, the remainder is used for validation. All three columns are standardized with the mean and standard deviation of the training split.

**Splitting the series into intervals.** `intervals_organization.py` slides a window over the series one record at a time. For each position it takes the previous 1008 records (7 days) and subsamples them with a step of 6, which yields 168 hourly time steps of 3 features per sample. The target is the next 144 temperature values, i.e. 24 hours ahead at the original 10-minute resolution.

**Inference.** The `narodmonitoring` package authenticates against the `narodmon.ru` API (`userLogon`) and requests one month of history (`sensorsHistory`) for three sensor ids specified in `.env`: pressure, temperature and humidity. The result is written to `csv_files/history_1month.csv`; the last 168 rows are written separately to `csv_files/history_7days.csv` and serve as the model input. `forecast.py` standardizes that window by its own mean and standard deviation, reshapes it to `(1, 168, 3)`, runs the prediction and converts the output back to degrees Celsius using the temperature statistics of the same window.

## Model

A sequential Keras model:

| Layer | Parameters |
| --- | --- |
| LSTM | 32 units, `return_sequences=True`, input shape `(168, 3)` |
| LSTM | 16 units, `activation='relu'` |
| Dense | 144 outputs (one per 10-minute step of the forecast horizon) |

Optimizer - RMSprop with `clipvalue=1.0`, loss - mean absolute error. Training runs for 10 epochs of 200 steps, batch size 256, shuffle buffer 10 000, 50 validation steps per epoch. The global random seed is fixed at 13. The trained model is saved in SavedModel format to `saved_model/AI_WeatherITSH-24H`. TensorFlow 2.11.1, Python 3.10.

## Limitations

- **The model is trained and applied on different data.** Training uses a single research-grade station in Jena; inference uses amateur sensors in the Moscow area. The third input channel is not the same either: air density during training, relative humidity at inference. Whether the model transfers across this gap was never verified.
- **There is no quantitative evaluation.** Only the training and validation loss were observed during fitting. No metric was measured on a held-out period, and the forecast was never compared against a baseline such as persistence.
- **Normalization at inference uses the statistics of the input window itself**, not the statistics stored from training, so identical weather can be scaled differently depending on the week.
- **Data handling is fragile.** Sensor histories are joined by row position with no time alignment or gap handling, and the pipeline stops if the API is unreachable.

Done differently today, the project would keep the same feature set on both sides and persist the training scaler, report MAE on a held-out period against a persistence baseline, and train on data from the same sensors that are used for the forecast.

## 🔧 Downloading and setting up

1. Make sure you have version of python `3.10.X` or higher.
2. Set up your environment (venv/conda etc... by your choice) and install all requirements.
3. Compile and train the model by simply running `model.py` script. (You can adjust model as you want, merely edit every needed variables)

Done... you've got a trained and fully capable of predicting model.

#### So how do we predict?

In this project, I used REST API from `https://narodmon.ru` site. To obtain the weather data, you have to set up some environment variables in `narodmonitoring\.env` file.
Before you do that, you must create an account there and get your api key, login and password.
Also, find any public sensors (pressure, temperature, humidity) then get their ids and insert into `narodmonitoring\.env` file.
Run `__init__.py`.

After when everything is done, run `forecast.py` script to get your forecast as matplot visualization.

## 📷 Screenshots

The screenshots below were produced by an earlier version of the model with a 12-hour horizon.

Weather forecast from 10:00 to 22:00 in 24.07.2022 (Moscow)

![10.00-22.00_24.07.22](https://github.com/Niron3206/AI_WeatherITSH/raw/master/10.00-22.00_24.07.22.png)

Weather forecast from 0:00 to 12:00 in 28.01.2023 (Moscow) (not so accurate temperature, depends on time of training model)

![0.00-12.00_28.01.23](https://github.com/Niron3206/AI_WeatherITSH/raw/master/0.00-12.00_28.01.23.png)

## License

MIT - see [LICENSE.md](./LICENSE.md).
