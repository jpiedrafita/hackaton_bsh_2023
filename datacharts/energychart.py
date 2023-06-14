import pandas as pd
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly
from entsoe import EntsoeRawClient
import pandas as pd


def plot_grap():
    data = pd.read_csv('datacharts/inoutdata1.csv')
    #data['ds'] = pd.to_datetime(data['ds'],format='%Y-%m-%d',dayfirst=True)
    data['ds'] = pd.to_datetime(data['ds'],dayfirst=False) ###RTX
    model = Prophet()
    model.fit(data)

    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)
    print (forecast)
    print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']])

    fig1 = model.plot(forecast)
    fig2 = model.plot_components(forecast)

    plot_plotly(model, forecast)
    plot_components_plotly(model, forecast)

    return forecast.to_json()
def plot_from_json(json):
    data = pd.read_json(json)
    #data['ds'] = pd.to_datetime(data['ds'],format='%Y-%m-%d',dayfirst=True)
    data['ds'] = pd.to_datetime(data['ds'],dayfirst=False) ###RTX
    model = Prophet()
    model.fit(data)

    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)
    print (forecast)
    print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']])

    fig1 = model.plot(forecast)
    fig2 = model.plot_components(forecast)

    plot_plotly(model, forecast)
    plot_components_plotly(model, forecast)

    return forecast.to_json()

