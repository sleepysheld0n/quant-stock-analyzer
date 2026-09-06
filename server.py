from flask import Flask, jsonify
from flask_cors import CORS
import yfinance as yf

app = Flask(__name__)
CORS(app)

@app.route("/stock/<ticker>")
def get_stock(ticker):
    data = yf.Ticker(ticker).history(period="3mo")

    if data.empty:
        return jsonify({"error": "No data found"}), 404

    latest_price = data["Close"].iloc[-1]
    previous_price = data["Close"].iloc[-2]
    daily_return = ((latest_price - previous_price) / previous_price) * 100

    ma20 = data["Close"].rolling(window=20).mean().iloc[-1]
    ma50 = data["Close"].rolling(window=50).mean().iloc[-1]
    last_30_days = data["Close"].tail(30).round(2).tolist()

    return jsonify({
        "ticker": ticker,
        "price": round(latest_price, 2),
        "daily_return": round(daily_return, 2),
        "ma20": round(ma20, 2),
        "ma50": round(ma50, 2),
        "history":last_30_days
    })

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)