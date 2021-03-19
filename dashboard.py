from datetime import date, timedelta

import streamlit as st
from yahoofinancials import YahooFinancials

import numpy as np 
import pandas as pd

ticker = st.text_input('Ticker', 'AAPL')
start_date = st.date_input("Start Date", date.today() - timedelta(days=365))
end_date = st.date_input("End Date", date.today())

yahoo_financials = YahooFinancials(ticker)

historical_stock_prices = yahoo_financials.get_historical_price_data(start_date.isoformat(), end_date.isoformat(), 'weekly')[ticker]['prices']
prices_df = pd.DataFrame.from_dict(historical_stock_prices)
prices_df['price'] = (prices_df['high'] + prices_df['low'])/2
prices_df = prices_df[["formatted_date", "price"]].set_index("formatted_date")

st.line_chart(prices_df)