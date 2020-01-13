from flask import jsonify, current_app, logging, make_response
import traceback
from http import HTTPStatus
from bs4 import BeautifulSoup as bs4
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys
import time
import json

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=options)

'''''''''''''''''
scrape
'''''''''''''''''
def scrape(scrape_data, headers_get_origin):
  result = make_result(scrape_data)
  response = make_response(jsonify(result))
  response.headers['Content-Type'] = 'application/json; charset=utf-8'

  # CORS対応 リクエストヘッダにOriginフィールドがある場合
  if headers_get_origin:
    response.headers['Access-Control-Allow-Origin'] = headers_get_origin
  
  return response

'''''''''''''''''
json request
'''''''''''''''''
def make_result(scrape_data):

  url = scrape_data['url']
  id = scrape_data['id']

  # url スクリーニング
  url = screening(url)

  # url 一意性
  url = uniqueness(url)

  # 24時間以内のキャッシュに問い合わせ
  scrape = scraped_cache(url, id)
  
  # キャッシュのスクレイピングを返す
  if scrape['cache_flag'] == True:
    return {scrape['json']}

  # 1.スクレイピング開始
  driver.get(url)
  html = driver.page_source.encode('utf-8')
  soup = bs4(html, "lxml") # "html.parser"よりもパースの速度が高速

  # 2.OGPタグを取得
  og_title = soup.find('meta', attrs={'property': 'og:title', 'content': True})
  og_description = soup.find('meta', attrs={'property': 'og:description', 'content': True})
  og_img = soup.find('meta', attrs={'property': 'og:image', 'content': True})

  # 3.ld+jsonを取得 + テキスト部を抽出する
  json_ld = {}
  if soup.find('script', type='application/ld+json'):
    json_text = soup.find('script', type='application/ld+json').text

    # 文字列をloads関数で辞書型にする
    json_ld = json.loads(json_text)

  # 4.全文取得からscriptやstyleを含む要素を削除する
  for script in soup(["script", "style"]):
    script.decompose()
  
  # テキストのみを取得=タグは全部取る
  body_text=soup.text

  # textを改行ごとにリストに入れて、リスト内の要素の前後の空白を削除
  lines= [line.strip() for line in body_text.splitlines()]

  # リストの空白要素以外をすべて文字列に戻す
  body_text = "".join(line for line in lines if line)

  return {
      'body_text': body_text,
      'url': url,
      'id': scrape_data['id'],
      'title': og_title['content'],
      'description': og_description['content'],
      'img': og_img['content'],
      't': int(time.time()),
      'JSONLD': json_ld,
  }

'''''''''''''''''
url screening
'''''''''''''''''
def screening(url):
  return url

'''''''''''''''''
url uniqueness
'''''''''''''''''
def uniqueness(url):
  return url

'''''''''''''''''
url scraped_cache
'''''''''''''''''
def scraped_cache(url, id):
  
  return {
    # キャッシュする時間をid毎で変更する
    'cache_flag': cache_time(id),
    # キャッシュからデータを返却する
    'json':{}
  }

'''''''''''''''''
cache time for publisher
'''''''''''''''''
def cache_time(id):
  return False
