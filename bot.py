import pandas as pd
import numpy as np


def calculate_ema(df, period):
    return df["close"].ewm(span=period, adjust=False).mean()


def analyze_market(df):
    if len(df) < 30:
        return {
            "signal": "WAIT",
            "confidence": 0,
            "reason": "Not enough candle data"
        }

    df = df.copy()

    # Moving averages
    df["ema9"] = calculate_ema(df, 9)
    df["ema21"] = calculate_ema(df, 21)

    # Recent candles
    last = df.iloc[-1]
    previous = df.iloc[-2]

    score = 0
    reasons = []

    # Trend
    if last["ema9"] > last["ema21"]:
        score += 1
        reasons.append("Short-term bullish trend")
    elif last["ema9"] < last["ema21"]:
        score -= 1
        reasons.append("Short-term bearish trend")

    # Candle momentum
    if last["close"] > last["open"]:
        score += 1
        reasons.append("Bullish candle")
    elif last["close"] < last["open"]:
        score -= 1
        reasons.append("Bearish candle")

    # Previous candle confirmation
    if last["close"] > previous["close"]:
        score += 1
        reasons.append("Price gaining momentum")
    elif last["close"] < previous["close"]:
        score -= 1
        reasons.append("Price losing momentum")

    # Signal
    if score >= 2:
        signal = "CALL"
    elif score <= -2:
        signal = "PUT"
    else:
        signal = "WAIT"

    confidence = min(abs(score) / 3 * 100, 100)

    return {
        "signal": signal,
        "confidence": round(confidence, 1),
        "score": score,
        "reason": ", ".join(reasons)
    }


def create_test_data():
    np.random.seed(42)

    prices = [100]

    for _ in range(49):
        change = np.random.normal(0, 0.5)
        prices.append(prices[-1] + change)

    data = []

    for i in range(1, len(prices)):
        open_price = prices[i - 1]
        close_price = prices[i]

        high = max(open_price, close_price) + abs(
            np.random.normal(0, 0.15)
        )

        low = min(open_price, close_price) - abs(
            np.random.normal(0, 0.15)
        )

        data.append([
            open_price,
            high,
            low,
            close_price
        ])

    return pd.DataFrame(
        data,
        columns=["open", "high", "low", "close"]
    )


if __name__ == "__main__":
    print("=" * 45)
    print("MARKET ANALYSIS BOT")
    print("=" * 45)

    candles = create_test_data()

    result = analyze_market(candles)

    print("\nSignal:", result["signal"])
    print("Confidence:", result["confidence"], "%")
    print("Score:", result["score"])
    print("Reason:", result["reason"])

    print("\nTest completed successfully.")
