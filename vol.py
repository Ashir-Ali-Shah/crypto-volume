import streamlit as st
import yfinance as yf
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt

# Set page config
st.set_page_config(page_title="Top Cryptocurrencies Analysis", layout="wide", page_icon="📈")

# Title of the Streamlit app
st.title("Top Cryptocurrencies by Trading Volume")
st.markdown("Explore the top 15 cryptocurrencies based on their trading volumes and year-over-year performance.")

# Sidebar for input to keep main area less cluttered
with st.sidebar:
    year = st.selectbox("Select Year", options=range(2023, 2017, -1), index=0)

# Define the start and end dates for the given year
start_date = dt.datetime(year, 1, 1)
end_date = dt.datetime(year, 12, 31)

# Define an extended list of cryptocurrencies (to ensure a broad selection for ranking)
cryptos = ['BTC-USD', 'ETH-USD', 'XRP-USD', 'BCH-USD', 'ADA-USD', 'LTC-USD', 'EOS-USD', 'BNB-USD',
           'XTZ-USD', 'XLM-USD', 'LINK-USD', 'TRX-USD', 'NEO-USD', 'IOTA-USD', 'DASH-USD',
           'DOT-USD', 'UNI-USD', 'DOGE-USD', 'SOL-USD', 'AVAX-USD']

# Fetch historical data
@st.cache_data(show_spinner=False)  # Cache the data for performance using the updated caching mechanism
def fetch_crypto_data(cryptos, start, end):
    crypto_data = {}
    for crypto in cryptos:
        data = yf.download(crypto, start=start, end=end)
        crypto_data[crypto] = data[['Adj Close', 'Volume']]
    return crypto_data

crypto_data = fetch_crypto_data(cryptos, start_date, end_date)

# Calculate average trading volume and price change for each cryptocurrency
average_volumes = {}
price_changes = {}
for crypto, data in crypto_data.items():
    if not data.empty:
        average_volumes[crypto] = data['Volume'].mean()
        price_changes[crypto] = ((data['Adj Close'][-1] - data['Adj Close'][0]) / data['Adj Close'][0]) * 100

# Sort cryptos by average volume in descending order and select top 15
top_cryptos = sorted(average_volumes, key=average_volumes.get, reverse=True)[:15]

# Display top cryptocurrencies, their average volume, and price change in a nicer format using metrics
st.subheader("Top 15 Cryptocurrencies by Trading Volume")
col1, col2, col3 = st.columns(3)
for i, crypto in enumerate(top_cryptos):
    with (col1 if i % 3 == 0 else col2 if i % 3 == 1 else col3):
        st.metric(label=crypto,
                  value=f"{average_volumes[crypto]:,.0f} volume",
                  delta=f"{price_changes.get(crypto, 0):.2f}% change")

# Visualization of the price data of the top cryptocurrencies with improved aesthetics
expander = st.expander("View Detailed Price Charts")
with expander:
    col1, col2 = st.columns(2)
    for i, crypto in enumerate(top_cryptos):
        with (col1 if i % 2 == 0 else col2):
            fig, ax = plt.subplots()
            ax.plot(crypto_data[crypto]['Adj Close'], label=f'{crypto} Adjusted Close', color='purple')
            ax.set_title(f"{crypto} Adjusted Close Price in {year}")
            ax.set_xlabel("Date")
            ax.set_ylabel("Adjusted Close Price (USD)")
            ax.legend()
            st.pyplot(fig)

# Uncomment the call to run the Streamlit app once the code is transferred to a suitable Python environment
# st.run()
