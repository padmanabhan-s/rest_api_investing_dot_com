from flask import Flask,jsonify
import requests
import random
user_agent_list = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]
from bs4 import BeautifulSoup 

def scraper():
    user_agent = random.choice(user_agent_list)
    headers = {'User-Agent': user_agent}
    page = requests.get("https://www.investing.com/indices/major-indices",headers = headers)
    if(page.status_code == 200):
        pass
    soup = BeautifulSoup(page.content,"html.parser")
    stock_market_table_body = soup.find("tbody")
    stock_market_rows = stock_market_table_body.findAll("tr")
    result = {}
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
    result = scraper()
    return jsonify(result)

@app.route('/<string:index>',methods = ["GET"])
def get_index(index):
    result = scraper()
    return jsonify(result[index])

if __name__ == "__main__":
    app.run(debug=True)