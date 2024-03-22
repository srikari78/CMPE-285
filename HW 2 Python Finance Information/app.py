from flask import Flask
from flask import render_template
from flask import request
from iexfinance.stocks import Stock
import yfinance as yf
from datetime import date, datetime
import calendar
import pandas as pd
import re

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('main.html')

    elif request.method == 'POST':

        error_message = ""
        tempData = {}
        try:
            # Input Fields
            ind1 = ind2 = ind3 = 0
            ticker = str(request.form['tickerSymbol'])
            ticker_length = len(ticker)
            if ticker_length == 1:
                ind1 = 5
                ind2 = -1
                ind3 = -4
            elif ticker_length == 2:
                ind1 = 6
                ind2 = -2
                ind3 = -4
            elif ticker_length == 3:
                ind1 = 7
                ind2 = -3
                ind3 = -4
            elif ticker_length == 4:
                ind1 = 8
                ind2 = -4
                ind3 = -4
            elif ticker_length == 5:
                ind1 = 9
                ind2 = -5
                ind3 = -4

            IEX_TOKEN = "pk_4ab28b0898d04a8090edc3bdc4a03903"

            stck = Stock(ticker, token=IEX_TOKEN)
            # stck = yf.Ticker(ticker)
            df = pd.DataFrame(data=stck.get_quote())
            current_date = str(date.today().strftime("%B %d"))
            current_time = str(datetime.now().strftime("%H:%M:%S"))
            current_day = str(date.today().strftime("%A"))
            current_year = str(date.today().strftime("%Y"))
            current_timezone = "PDT"
            company_name = df["companyName"].to_string()
            stock_symbol = df["symbol"].to_string()
            stock_price1 = df["latestPrice"].to_string()
            stock_price = re.findall("-?\+?\d+\.\d+", stock_price1)
            value_change1 = df["change"].to_string()
            value_change = re.findall("-?\+?\d+\.\d+", value_change1)
            prev_close1 = df["previousClose"].to_string()
            prev_close = re.findall("-?\+?\d+\.\d+", prev_close1)
            perc_change1 = df["changePercent"].to_string()
            perc_change2 = re.findall("-?\+?\d+\.\d+", perc_change1)
            perc_change3 = round((float(perc_change2[0])) * 100, 4)
            perc_change = str(perc_change3)

            pm = ""
            if float(value_change[0]) > 0:
                pm = "+"
            elif float(value_change[0]) < 0:
                pm = ""

            br_open = "("
            br_close = ")"
            perc = "%"

            tempData = {'tickerSymbol': ticker, 'currentDay': current_day,
                        'currentDate': current_date, 'currentTime': current_time,
                        'companyName': company_name[ind1:], 'currentYear': current_year,
                        'currentTimezone': current_timezone, 'bropen': br_open, 'brclose': br_close,
                        'stockSymbol': stock_symbol[ind2:], 'stockPrice': stock_price[0],
                        'valueChange': value_change[0], 'percChange': perc_change,
                        'pm': pm, 'errorMessage': error_message, "perc": perc}

        except:
            error_message = "Error Fetching your data, kindly ensure you entered a valid symbol!"

            # Fetch Data

        return render_template('main.html', **tempData)


if __name__ == '__main__':
    app.run(debug=True)