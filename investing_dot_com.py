from flask import Flask,jsonify   # Flask is microframework
import requests                   # To make a http request
from bs4 import BeautifulSoup     # To parse html pages
import random                     # To select random headers for requests 
user_agent_list = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]                                 # headers for requests to mimic human rather than scraping

def scraper():                    # Main scraper function to scrape investing.com
    user_agent = random.choice(user_agent_list)
    headers = {'User-Agent': user_agent}
    page = requests.get("https://www.investing.com/indices/major-indices",headers = headers)
    if(page.status_code == 200):                                                             # checking for ssuccessful requests
        pass
    soup = BeautifulSoup(page.content,"html.parser")                                         # parsing the html page
    stock_market_table_body = soup.find("tbody")                     # whole major indices table
    stock_market_rows = stock_market_table_body.findAll("tr")        # each row in the table
    result = {}                                                      # the result to be returned from the function
    for rows in stock_market_rows:
        each_rows = {}
        each_rows["flag"] = rows.find("td",{'class':"flag"}).find("span").get("title")
        temp = rows.findAll("td")
        
        each_rows["Last"] = temp[2].text
        each_rows["High"] = temp[3].text
        each_rows["Low"] = temp[4].text
        each_rows["Chg."] = temp[5].text
        each_rows["Chg.%"] = temp[6].text
        Index = temp[1].text
        result[Index] = each_rows
        
    return result


app = Flask(__name__)
@app.route('/')
def index():
    result = scraper()                # result from scraper function
    return jsonify(result)            # returning the result of scraper function to the user 


if __name__ == "__main__":
    app.run(debug=True)              # to run in local machine
    #app.run(debug = False,host= '0.0.0.0' ,port = 8080)        # host and port have to be yours own application host and port