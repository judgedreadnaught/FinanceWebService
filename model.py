import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
from dateutil.relativedelta import relativedelta
from pandas_datareader import data as pdr
import math

yf.pdr_override()
# Creating exponential moving averages
emasUsed = [3, 5, 8, 10, 12, 15, 30, 35, 40, 45, 50, 60]  # smoothing is 2
data = None  # initializing the data frame that gets yahoo finance data
now = dt.date.today()  # initializing the now time to today
starting_dates = ["1Y", "2Y", "3Y", "4Y", "5Y"]


def calcDate(date):
    date = date[0:1]
    newDate = now - relativedelta(years=int(date))  # + dt.timedelta(days=1)
    return newDate


def makeEma(data, emasUsed, stock):
    try:
        for ema in emasUsed:
            data["Ema_" + str(ema)] = round((data.iloc[:, 4].ewm(int(ema), adjust=False)).mean(), 2)
        st.subheader("EMA DATA FOR STOCK: " + stock)
        st.write(data.iloc[:, 6:])
        return data
    except ValueError:
        print()



def calc_position(data, pos, row_tracker,simu):
    #new_df = pd.DataFrame(columns=["Position Value", "Exit Position"])
    df_buying = []
    df_selling = []
    df_change = []
    date_bought = []
    date_sold = []
    for i in data.index:
        minV = min(data["Ema_3"][i], data["Ema_5"][i], data["Ema_8"][i],
                   data["Ema_10"][i], data["Ema_12"][i], data["Ema_15"][i])
        #st.write("Min V: " + str(minV))
        maxV = max(data["Ema_30"][i], data["Ema_40"][i], data["Ema_45"][i],
                   data["Ema_50"][i], data["Ema_60"][i])
        #st.write("Max V: " + str(maxV))
        closeV = data["Adj Close"][i]
        #st.write("Close V: " + str(closeV))
        if (minV > maxV):
            if pos == 0:
                pos = 1
                buying = closeV
                #st.write(str(buying))
                # we do not grow a data frame, instead we create a dictionary of values and then create a data frame at
                # the end using that dictionary
                date_bought.append(str(i.to_pydatetime())[:10])
                df_buying.append(buying)
                #st.write(df_buying)
                #st.write("Buying")
        elif (maxV > minV):
            if pos == 1:
                pos = 0
                selling = closeV
                #st.write("Selling")
                profit = round(((selling - buying) / buying) * 100,2)
                df_change.append(profit)
                df_selling.append(selling)
                # strfttime() converts datetime into a string
                date_sold.append(str(i.to_pydatetime())[:10])

        elif (row_tracker == data["Adj Close"].count() - 1 and pos == 1):
            pos = 0
            selling = buying
            profit = round(((selling - buying) / buying) * 100,2)
            df_change.append(profit)
            df_selling.append(selling)
            date_sold.append(str(i.to_pydatetime())[:10])
        row_tracker = row_tracker + 1
    #st.write(df_buying)
    # st.write(df_selling)
    new_df = pd.DataFrame({"Position": df_buying})

    """adding a list of different length with a filler"""
    filler = 0
    st.title("BACKTESTER")
    st.subheader("Results of Trading")
    new_df.loc[:,"Selling"] = df_selling + [filler] * (len(new_df.index) - len(df_selling))
    new_df.loc[:,"Percent Change"] = df_change + [filler] * (len(new_df.index) - len(df_change))
    new_df.loc[:,"Date Bought"] = date_bought + [filler] * (len(new_df.index) - len(date_bought))
    new_df.loc[:,"Date Sold"] = date_sold + [str([filler] * (len(new_df.index) - len(date_bought)))]
    st.write(new_df)

    st.subheader("Summarized Data")
    sum = 0.0
    pos = 0
    neg = 0
    for i in new_df["Percent Change"]:
        x = float(i)
        if (x > 0):
            pos = pos + 1
        elif (x < 0):
            neg = neg + 1
        else:
            pos = pos + 0
        sum = sum + x
    st.write("Percentage Gain percentage:   " + str(round(sum,3)) + "%")
    st.write("Total Number of Gains: " + str(pos))
    st.write("Total Number of Losses: " + str(neg))
    simu_gain = float((simu * ((round(sum,3))/100)) + simu)
    st.write("Starting Fund: $" + str(simu))
    st.write("Ending Fund: $" + str(round(simu_gain,2)))



def app():

    st.title('TA For Leveraged ETFs and Stocks')

    st.write('Tests the red, white blue TA strategy for stocks and '
             'leverged ETFs using data from one to five years ago ')

    user_stock = st.text_input('Enter Stock Ticker Symbol').upper()  # initially going to be blank or none
    select_date = st.selectbox("Select the Starting Date For Calculations", starting_dates)
    simulated_money = st.number_input("Enter Simulated Amount of Trading Money")

    other_date = select_date
    select_date = calcDate(select_date)
    try:
        data = pdr.get_data_yahoo(user_stock, select_date, now)
        st.subheader(str(user_stock) + " Data")
        st.write(data)
        data = makeEma(data, emasUsed, user_stock)
        row_tracker = 0  # if we reach the last date we exit our position
        pos = 0  # do we already have a position?
        calc_position(data,pos,row_tracker,simulated_money)

    # [3, 5, 8, 10, 12, 15, 30, 35, 40, 45, 50, 60]

    except ValueError:
        st.write("")
