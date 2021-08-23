# FinanceWebService

This is a finanical service website I built using python. The libraries that were the foundation for this project were pandas, yfinance, and streamlit.
I utilized a variation of streamlit that allowed one to host multiple webpages without the use of "if" statements to hide the page. 

The first page allows one to view basic information about a stock, but also calculates the stocks SMA (Simple Moving Average) up to a designated date 200 days ago.
The current SMA, 52 Week High, and 52 Week low are displayed, and if the user selects to view stock data past one month, a graph of all the closing prices of that 
stock, up until the selected date, will appear.

The second page calculates the Pivot Points and Bollinger Bands of a stock up to a certain date range. One can select what SMA to use for the stock as well. 
One can view the stock data and SMA_(10-50) data just like the previous page. The user then has the ability to select the standard deviation for their 
Bollinger Bands, after which the lower and upper bolinger band calculations are displayed in a dataframe. A graph of the Bollinger Bands, SMA_(10-20), and
Adjusted Close Price is then displayed. Below the graph is a dataframe listing the pivot and support points of the stock. The final dataframe is the backtester, 
which algorithmically trades the stock whenever it crosses above the upper bollinger band, and below the lower bollinger band. It lists the price and date at which
it was either bought or sold. There is a percentage change displayed for each trade and a gross percent change is calculated and displayed at the end. 

The third page is TA for leveraged ETFs and Stocks. One has the option of inputting in a stock ticker symbol and then selecting how many years, 1-5, they would
like to go back to for calculations. Then one can also enter a simulated amount of trading money. Below the displayed stock data, there is a data frame for the 
EMA (Exponential Moving Average) for the stock. The EMA data is for EMA_3 through EMA_60, so exponential moving average of 3 days,5 days,..., 60 days. The website
then algorithmically trades based a set of criteria and lists the price and date at which the stock was bought or sold. It then calculates the percent change and logs
the total percent gain, number of gains and losses, and the starting and ending fund. 

The final page is an unusual volume detector that checks if the volume of any stock in the Dow Jones deviates a certain aomunt from the mean. The program uses the
data of a stock from up to two weeks ago to calculate the mean. Then for each stock in the Dow Jones a data frame of the stock is displayed and above the data frame
the stock name, stock volume of today, mean, standard dev, and the volume it must exceed to be considered "abonormal" is displayed. If there are unusual amounts of volume
the website then displays a bolded text alerting the user. 
