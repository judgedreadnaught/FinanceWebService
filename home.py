import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
from dateutil.relativedelta import relativedelta
from pandas_datareader import data as pdr


# print(dt.date.today())

yf.pdr_override()
dates = ("1D", "1W", "1M", "3M", "1Y", "5Y")
smas = ("50", "100", '150', '200')
counter = 0

def getStock(stock, start):
    try:
        today = dt.datetime.today()
        data = pdr.get_data_yahoo(stock, start, today)
        st.header(str(stock))
        st.write(data)
        st.header(str(stock) + " Simple Moving Average")
    except ValueError:
        st.write("")

def getDate(date):
    now = dt.date.today()
    start = now
    if date == "1D":
        start = start - dt.timedelta(days=1)
    elif date == "1W":
        start = start - dt.timedelta(weeks=1)
    elif date == "1M":
        start = start - relativedelta(months=1)
    elif date == "3M":
        start = start - relativedelta(months=3)
    elif date == "1Y":
        start = start - relativedelta(years=1)
    elif date == "5Y":
        start = start - relativedelta(years=5)
    return start


def app():
    st.title('STOCK INFO')
    st.write('Retrieves and formats stock data from yahoo finance and calculates the simple moving average of the '
             'selected amount of days')

    user_stock = st.text_input('Enter Stock Ticker Symbol').upper()
    date = st.selectbox("Enter Start Date For Stock Data (Change date to access graph)", dates)
    start_date = getDate(date)
    getStock(user_stock, start_date)
    data = None

    try:
        sma_days = st.selectbox("Select Simple Moving Average Day Criteria", smas)
        now = dt.date.today()
        sma_date = now - dt.timedelta(days=int(sma_days) * 2)  # Need to do this because a stock doesnt have enough data to calc the
        #  moving average the first 50,100, whatever days
        #st.write(sma_date)
        data = pdr.get_data_yahoo(user_stock, sma_date, now)
        data["SMA"] = data.iloc[:,4].rolling(int(sma_days) + 1).mean()
        st.subheader(sma_days + " Day Simple Moving Average of " + user_stock )
        st.write(data["SMA"].iloc[int(sma_days):])
        graph = yf.download(user_stock,start_date,now)["Close"]
        if (str(date) != "1D" and str(date) != "1W"):
            st.subheader("Graph of " + user_stock + " Closing Values from " + str(start_date) + " to " +
                         str(now))
            st.line_chart(graph)

    except ValueError:
        st.write("")

    """ Stock Screener """

    try:
        if (data is not None):
            sma_Value = round(data["SMA"][-1], 3)
            st.subheader("Current SMA Value: " + str(sma_Value))
            data = pdr.get_data_yahoo(user_stock, now - relativedelta(years=1),now)
            week_min = min(data["Low"])  # 260 == 5 * 52 because 5 trading days
            week_max = max(data["High"])
            st.subheader("52 Week High: " + str(round(week_max,3)))
            st.subheader("52 Week Low: " + str(round(week_min,3)))

    except ValueError:
        st.write("")

