# app.py
import streamlit as st
import yfinance as yf
import pandas as pd
import joblib
from generate_features import generate_features

# Load model and scaler
model = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")

# Ticker map: Ticker → Company Name
company_map = {
    "AAPL": "Apple Inc.",
    "MSFT": "Microsoft Corp.",
    "GOOGL": "Alphabet Inc.",
    "AMZN": "Amazon.com Inc.",
    "TSLA": "Tesla Inc."
}

tickers = list(company_map.keys())
company_names = list(company_map.values())

# Invert map for reverse lookup
company_to_ticker = {v: k for k, v in company_map.items()}

# --- Streamlit UI ---

st.set_page_config(page_title="Stock Movement Predictor", layout="centered")
st.title("📈 Financial Stock Movement Prediction")
st.markdown("This app uses an SVM model trained on 3 years of stock data to predict **tomorrow's movement** based on recent trends.")

# Select company
selected_company = st.selectbox("🔍 Choose a Company", company_names)
selected_ticker = company_to_ticker[selected_company]

# Show current chart
data = yf.download(selected_ticker, period="21d", interval="1d", auto_adjust=True)
if not data.empty:
    st.subheader(f"{selected_company} - Last 21 Days Close Price")
    st.line_chart(data['Close'])
    # st.pyplot(plt)
    st.caption("📌 All prices are shown in USD ($)")

# Predict
if st.button("🚀 Predict Tomorrow's Movement"):
    if len(data) < 15:
        st.error("❌ Not enough recent data to make a prediction.")
    else:
        # Generate features
        returns = data['Close'].pct_change().dropna()
        features = generate_features(returns)

        if features.empty:
            st.error("❌ Unable to generate features from recent data.")
        else:
            # Add ticker_encoded
            ticker_encoded = tickers.index(selected_ticker)
            features['ticker_encoded'] = ticker_encoded

            # Scale and predict
            scaled_input = scaler.transform(features)
            prediction = model.predict(scaled_input)[0]

            # Show result
            st.markdown("### 🧠 Model Prediction")
            if prediction == 1:
                st.success("📈 Tomorrow's Movement: **UP**")
            else:
                st.warning("📉 Tomorrow's Movement: **DOWN**")
