from bs4 import BeautifulSoup
import json
import requests
import re

BASE = 'https://finance.yahoo.com'
# user-agent for chrome
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'}

def current_market_price(symbol):
  page = requests.get(BASE + f"/quote/{symbol}", headers=HEADERS)
  soup = BeautifulSoup(page.content, 'html.parser')
  current_market_price = soup.find("fin-streamer", {"data-symbol":symbol.upper()})
  res = current_market_price.text if (current_market_price) else f"Can't find {symbol}"
  return res

def company_details(symbol):
  page = requests.get(BASE + f"/quote/{symbol}", headers=HEADERS)
  soup = BeautifulSoup(page.content, 'html.parser')
  scripts = soup.find('body').find_all('script')
  # search json "context" object in all script tags
  dataStr = ''
  for val in scripts:
      test = str(val)
      if '{"context":' in test:
          dataStr = test
          break
  # easy way to find the end of the json object
  dataStr = dataStr.replace('''"td-app-finance"}}}};''', '''"td-app-finance"}}}}###;''')
  # now get json object using regex
  reg = re.search(r"(?={\"context)(.*?)(?=###;)", dataStr)
  res = f"Can't find {symbol}"
  if reg:
    jsonStr = json.loads(reg.group(1))
    res = jsonStr['context']['dispatcher']['stores']['QuoteSummaryStore']
  
  return res