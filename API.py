from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from flask import Flask, jsonify
from Webhook import send_messages, send_html
from ORM import Operations
from random import randint
from time import sleep
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException


app = Flask(__name__)
'''
driver = webdriver.Remote("http://192.168.1.35:4444/wd/hub", DesiredCapabilities.FIREFOX)
driver.get('https://www.upwork.com/search/jobs/?q=scrap&sort=recency')
'''
options = Options()
options.headless = False
driver = webdriver.Firefox(options=options, executable_path='/usr/bin/geckodriver')
driver.get('https://www.upwork.com/search/jobs/?page=2&q=scrap&sort=recency')

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

# new and improved, does only use selenium, not bs4
def new_parse():
  listed_ads = []
  try:
    ads = driver.find_elements_by_xpath("//section[@class='air-card air-card-hover job-tile-responsive ng-scope']")
    for ad in ads:
      result = {}

      try:
        title = ad.find_element_by_tag_name("a")
        url = title.get_attribute('href')

        result["title"] = title.text
        result["url"] = url
        result["id"] = url.split('~')[-1].replace('/', '')
      except NoSuchElementException:
        print('Fail to load item from list')

      try:

        payments = ad.find_elements_by_tag_name("strong")
        payment = '-'.join([x.text for x in payments])
        result["payment"] = payment

      except NoSuchElementException:
        print('Fail to load payment from item in list')

      listed_ads.append(result)


    # filter from results new ads
    old_ads = Operations.GetAllIds()
    new_ads = [ad for ad in listed_ads if ad['id'] not in old_ads]

    for ad in new_ads:
      driver.get(ad["url"])

      try:
        sections = driver.find_elements_by_xpath("//section[@class='up-card-section']")
        body = sections[1].text
        ad["body"] = body

      except NoSuchElementException:
        print("Fail to load body")

    if len(new_ads) is not 0:
      [Operations.SaveAd(ad) for ad in new_ads]
      send_messages(new_ads)


  except NoSuchElementException:
    print('Fail to load list')

  for ad in listed_ads:
    print(ad)

# to be deleted
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
  return new_parse()

@app.route('/update')
def update():
  sleep(randint(0,60))
  return new_parse()

@app.route('/msg')
def msg():

  ads = [{'id': '01d33e2d5b0742ea28', 'title': 'Lead generation to find MSPs in USLead generation to find MSPs in US', 'url': 'https://www.upwork.com/job/Lead-generation-find-MSPs_~01d33e2d5b0742ea28/', 'payment': 'Fixed: $10'}]
  send_messages(ads)

  return jsonify(ads)

@app.route('/getads')
def getAds():
  return jsonify([x.Readable() for x in Operations.GetAll()])

if __name__ == "__main__":
  listed_ads = []
  try:
    ads = driver.find_elements_by_xpath("//section[@class='air-card air-card-hover job-tile-responsive ng-scope']")
    for ad in ads:
      result = {}

      try:
        title = ad.find_element_by_tag_name("a")
        url = title.get_attribute('href')

        result["title"] = title.text
        result["url"] = url
        result["id"] = url.split('~')[-1].replace('/', '')
      except NoSuchElementException:
        print('Fail to load item from list')

      try:

        payments = ad.find_elements_by_tag_name("strong")
        payment = '-'.join([x.text for x in payments])
        result["payment"] = payment

      except NoSuchElementException:
        print('Fail to load payment from item in list')

      listed_ads.append(result)


    # filter from results new ads
    old_ads = Operations.GetAllIds()
    new_ads = [ad for ad in listed_ads if ad['id'] not in old_ads]

    for ad in new_ads:
      driver.get(ad["url"])

      try:
        sections = driver.find_elements_by_xpath("//section[@class='up-card-section']")
        body = sections[1].text
        ad["body"] = body

      except NoSuchElementException:
        print("Fail to load body")

    if len(new_ads) is not 0:
      [Operations.SaveAd(ad) for ad in new_ads]
      send_messages(new_ads)





  except NoSuchElementException:
    print('Fail to load list')

  for ad in listed_ads:
    print(ad)