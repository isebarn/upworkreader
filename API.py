from bs4 import BeautifulSoup
from flask import Flask, jsonify
from ORM import Operations
from random import randint
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from Webhook import send_messages, send_html
import os

app = Flask(__name__)

BASE_URL = 'https://www.upwork.com/search/jobs/?q={}&sort=recency'
driver = webdriver.Remote(os.environ.get('BROWSER'), DesiredCapabilities.FIREFOX)
environment = os.environ.get('ENVIRONMENT')

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
def new_parse(search_terms):
  listed_ads = []
  errors = []
  logs = []

  for search_term in search_terms:

    driver.get(BASE_URL.format(search_term))
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
          errors.append({ 'error': 'Fail to load item from list' })

        try:
          payments = ad.find_elements_by_tag_name("strong")
          payment = '-'.join([x.text for x in payments])
          result["payment"] = payment

        except NoSuchElementException:
          errors.append({ 'error': 'Fail to load payment from item in list' })

        listed_ads.append(result)

    except NoSuchElementException:
      errors.append({ 'error': 'Fail to load list' })


  unique_ads = {x["id"]: x for x in listed_ads}
  unique_listed_ads = list(unique_ads.values())
  unique_listed_ads = unique_listed_ads

  old_ads = Operations.GetAllIds()
  new_ads = [ad for ad in unique_listed_ads if ad['id'] not in old_ads]
  new_ads = new_ads[0:3]

  for ad in new_ads:
    driver.get(ad["url"])
    body = ''

    try:
      if environment == 'development':
        sections = driver.find_elements_by_xpath("//section[@class='up-card-section']")
        body = sections[1].text

      if environment == 'server':
        child_element =  WebDriverWait(driver,10).until(
        lambda x: x.find_element_by_xpath("//section/div[@class='break mb-0']"))
        body = child_element.text

    except NoSuchElementException:
      error.append({ 'error': "Fail to load body" })

    except Exception as e:
      error.append({ 'error': e })

    ad["body"] = body


  if len(new_ads) is not 0:
    [Operations.SaveAd(ad) for ad in new_ads]
    send_messages(new_ads)

  if len(errors) > 0:
    error_data = {}
    error_data["errors"] = errors
    Operations.LogError(errors)

  if len(logs) > 0:
    log_data = {}
    log_data["new_saved_ads"] = len(new_ads)
    log_data["new_unique_ads"] = len(unique_listed_ads)
    Operations.LogUpdate(log_data)

  return new_ads

@app.route('/')
def root():
  return 'Hello'

@app.route('/busted')
def busted():
  return jsonify({ "busted": is_busted() })

@app.route('/testupdate')
def testupdate():
  return new_parse(['scrap'])

@app.route('/update')
def update():
  search_terms = Operations.GetAllKeywords()
  return jsonify(new_parse(search_terms))

@app.route('/msg')
def msg():
  ad = {}
  ad['id'] = '01d33e2d5b0742ea28'
  ad['title'] = 'Lead generation to find MSPs in USLead generation to find MSPs in US'
  ad['url'] = 'https://www.upwork.com/job/Lead-generation-find-MSPs_~01d33e2d5b0742ea28/'
  ad['payment'] = 'Fixed: $10'
  ad['body'] = 'heh'
  ads = [ad]
  send_messages(ads)

  return jsonify(ads)

@app.route('/getads')
def getAds():
  return jsonify([x.Readable() for x in Operations.GetAll()])

if __name__ == "__main__":
  search_terms = Operations.GetAllKeywords()
  print(new_parse(search_terms))