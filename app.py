import streamlit as st
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

st.set_page_config(page_title="Twitter Sentiment Analysis with Forecasting", layout="wide")

st.title("🔍 Twitter Sentiment Analysis + ARIMA Forecasting")

# Upload CSV
uploaded_file = st.file_uploader("📂 Upload your Tweets CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Ensure "tweet" column exists
    if "tweet" not in df.columns:
        st.error("❌ CSV must contain a 'tweet' column")
    else:
        st.write("✅ Data Preview:", df.head())

        # Sentiment Analysis
        sentiments = []
        for text in df["tweet"]:
            blob = TextBlob(str(text))
            polarity = blob.sentiment.polarity
            sentiment = "Positive" if polarity > 0 else "Negative" if polarity < 0 else "Neutral"
            sentiments.append([text, sentiment, round(polarity, 2)])

        result_df = pd.DataFrame(sentiments, columns=["Tweet", "Sentiment", "Polarity"])

        st.subheader("📊 Sentiment Results")
        st.dataframe(result_df)

        # Sentiment distribution
        sentiment_counts = result_df["Sentiment"].value_counts()
        st.bar_chart(sentiment_counts)

        # --- Simulate Date column ---
        result_df["Date"] = pd.date_range(start="2023-01-01", periods=len(result_df), freq="D")

        # Aggregate daily sentiment
        daily_sentiment = result_df.groupby("Date")["Polarity"].mean()

        st.subheader("📈 Sentiment Trend Over Time")
        st.line_chart(daily_sentiment)

        # --- ARIMA Forecasting ---
        st.subheader("🔮 ARIMA Forecasting of Sentiment Polarity")

        try:
            model = ARIMA(daily_sentiment, order=(2,1,2))
            model_fit = model.fit()

            forecast = model_fit.forecast(steps=7)

            forecast_df = pd.DataFrame({
                "Date": pd.date_range(start=daily_sentiment.index[-1] + pd.Timedelta(days=1), periods=7),
                "Forecasted Polarity": forecast
            })

            st.write(forecast_df)

            fig, ax = plt.subplots()
            daily_sentiment.plot(ax=ax, label="Historical")
            forecast_df.set_index("Date")["Forecasted Polarity"].plot(ax=ax, label="Forecast", linestyle="--")
            ax.legend()
            st.pyplot(fig)

        except Exception as e:
            st.warning(f"⚠️ Could not run ARIMA forecasting: {e}")
