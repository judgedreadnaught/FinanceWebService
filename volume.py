import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
from dateutil.relativedelta import relativedelta
from pandas_datareader import data as pdr
import math
from pandas_datareader import data as pdr
import yahoo_fin
import yahoo_fin.stock_info as si

yf.pdr_override()
start_dates = ["1D","2D","3D","4D","5D","1W","2W"]
std_devs = [2,3,4,5,6,7,8,9,10,11,12,13,14,15]
now = dt.date.today()
dow_info = []
dow_data = pd.DataFrame()


def calcDate(date):
    new_date = None
    if (date == "1W"):
        new_date = 7
    elif (date == "2W"):
        new_date = 14
    else:
        day = date[0:1]
        new_date = int(day)
    return new_date
def app():

    st.title("Unusual Volume of Dow Jones Stocks")
    dow_list = si.tickers_dow()
    st.subheader("Checks if the volume of any stock in the Dow Jones deviates"
                 " a certain amount from the mean. This program uses the data of "
                 "a stock from up to two weeks ago to calculate the mean.")
    #stock = st.selectbox("Select a stock from this list. All stocks are "
    #                    "listed in the Dow Jones", dow_list)
    start_date = st.selectbox("Select how far back you would like to check the "
                              "volume",start_dates)
    dev = float(st.selectbox("Select the standard deviation you would like to apply to the calculations",
                       std_devs))
    temp_date = calcDate(start_date)
    counter = 0
    for ticker in dow_list:
        #dow_info.append(si.get_data(ticker,date))
        #st.write(str(type(si.get_data(ticker,date))))
        #st.write(dow_info[counter])

        date = now - relativedelta(weeks=2)
        # This is all just visual data
        temp_df = si.get_data(ticker,date) # gets the data up to two weeks ago
        stock_name = temp_df.iloc[0, -1]
        stock_vol = temp_df.iloc[-1,5]  # current volume
        # specified that they wanted to see

        # calc the std_dev stuff
        std_dev = 0.0
        mean = temp_df.iloc[:,5].mean()

        for num in temp_df.iloc[:,5]:
            std_dev += math.pow(float(num) - mean, 2)
        std_dev = math.sqrt(std_dev/len(temp_df["volume"]))

        st.write("Stock Name: " + stock_name)
        st.write("Stock Volume Today: " + str(stock_vol))
        st.write("Mean is: " + str(mean))
        st.write("Standard Dev is: " + str(round(std_dev,3)))
        deviation = (dev * std_dev) + mean
        st.write("The Volume must exceed: " + str(round(deviation,0)))
        if (deviation <= stock_vol):
            st.title("Unsual Volume")
        else:
            st.write("Not Unusual Amounts of Volume")
        st.write(temp_df.iloc[-temp_date:, :])  # prints from the two week data just up til the date they

        counter = counter + 1
