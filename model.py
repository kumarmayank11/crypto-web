import yfinance as yf
import pandas as pd
from prophet import Prophet
import os

def predict_stock_price(ticker, days=7):
    df = yf.download(ticker, period="6mo", interval="1d")
    df.reset_index(inplace=True)
    df = df[['Date', 'Close']]
    df.rename(columns={"Date": "ds", "Close": "y"}, inplace=True)

    model = Prophet()
    model.fit(df)

    future = model.make_future_dataframe(periods=days)
    forecast = model.predict(future)

    forecast_data = forecast[['ds', 'yhat']].tail(days)
    forecast_data.columns = ['Date', 'Predicted Price']

    os.makedirs("predictions", exist_ok=True)
    filename = f"predictions/{ticker.upper()}_forecast.csv"
    forecast_data.to_csv(filename, index=False)

    return forecast_data, filename
