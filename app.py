from flask import Flask, render_template, request, send_file
from model import predict_stock_price

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    ticker = request.form['ticker']
    forecast_data, csv_path = predict_stock_price(ticker)

    dates = forecast_data['Date'].dt.strftime('%Y-%m-%d').tolist()
    prices = forecast_data['Predicted Price'].round(2).tolist()

    return render_template('result.html', ticker=ticker.upper(), dates=dates, prices=prices, csv_path=csv_path)

@app.route('/download/<path:csv_path>')
def download(csv_path):
    return send_file(csv_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
