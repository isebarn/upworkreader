from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from flask import Flask, jsonify
from Webhook import send_messages
from ORM import Operations
from random import randint
from time import sleep

app = Flask(__name__)
driver = webdriver.Remote("http://192.168.1.35:4444/wd/hub", DesiredCapabilities.FIREFOX)
driver.get('https://www.upwork.com/search/jobs/?q=scrap&sort=recency')

def is_busted():
  soup = BeautifulSoup(driver.page_source, "lxml")
  restricted_access_divs = soup.find_all("div", class_="page-title")

  if len(restricted_access_divs) == 1:
    restricted_access_div = restricted_access_divs[0]
    texts = restricted_access_div.findChildren('h1')

    if len(texts) == 1:
      if texts[0].text == 'Please verify you are a human':
        return True

  return False

def parse():
    driver.refresh()
    soup = BeautifulSoup(driver.page_source, "lxml")

    if is_busted():
      return jsonify({ "busted": True })

    ads = soup.find_all("a", class_="job-title-link break visited")

    new_ads = []
    parsed_ads = []

    for ad in ads:

      fixed = ad.findNext('strong', class_="js-budget")
      if fixed is not None:
        fixed = fixed.text.replace(' ', '').replace('\n', '')

      payment_type = ad.findNext('strong').text.replace(' ', '').replace('\n', '')

      if 'Hourly' in payment_type:
        payment = payment_type

      else:
        payment = 'Fixed: {}'.format(fixed)

      result = {}
      result['id'] = ad['href'].split('~')[-1].replace('/', '')
      result['title'] = ad.text.replace('\n', '')
      result['url'] = 'https://www.upwork.com{}'.format(ad['href'])
      result['payment'] = payment

      parsed_ads.append(result)

    if len(parsed_ads) is not 0:
      old_ads = Operations.GetAllIds()

      new_ads = [ad for ad in parsed_ads if ad['id'] not in old_ads]

      if len(new_ads) is not 0:
        [Operations.SaveAd(ad) for ad in new_ads]
        send_messages(new_ads)

    return jsonify(new_ads)

@app.route('/busted')
def busted():
  return jsonify({ "busted": is_busted() })

@app.route('/testupdate')
def testupdate():
  return parse()

@app.route('/update')
def update():
  sleep(randint(0,60))
  return parse()

@app.route('/msg')
def msg():

  ads = [{'id': '01d33e2d5b0742ea28', 'title': 'Lead generation to find MSPs in USLead generation to find MSPs in US', 'url': 'https://www.upwork.com/job/Lead-generation-find-MSPs_~01d33e2d5b0742ea28/', 'payment': 'Fixed: $10'}]
  send_messages(ads)

  return jsonify(ads)

@app.route('/getads')
def getAds():
  return jsonify([x.Readable() for x in Operations.GetAll()])

if __name__ == "__main__":
  driver.refresh()
  soup = BeautifulSoup(driver.page_source, "lxml")
  restricted_access_divs = soup.find_all("div", class_="page-title")

  if len(restricted_access_divs) == 1:
    restricted_access_div = restricted_access_divs[0]
    texts = restricted_access_div.findChildren('h1')

    if len(texts) == 1:
      print(texts[0].text == 'Please verify you are a human')
