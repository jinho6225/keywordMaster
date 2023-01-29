from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests, bs4
import time, os
from . import signaturehelper
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('../../.env')
load_dotenv(dotenv_path=dotenv_path)

def get_header(method, uri, api_key, secret_key, customer_id):
	timestamp = str(round(time.time() * 1000))
	signature = signaturehelper.Signature.generate(timestamp, method, uri, SECRET_KEY)
	return {
	 'Content-Type': 'application/json; charset=UTF-8',
	 'X-Timestamp': timestamp,
	 'X-API-KEY': API_KEY,
	 'X-Customer': str(CUSTOMER_ID),
	 'X-Signature': signature
	}

BASE_URL = os.getenv('BASE_URL')
API_KEY = os.getenv('API_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')
CUSTOMER_ID = os.getenv('CUSTOMER_ID')

uri = '/keywordstool'
method = 'GET'
naver_shopping_url = "https://search.shopping.naver.com/search/all?&cat_id=&frm=NVSHATC&query="
daum_blog_url = "https://search.daum.net/search?w=blog&lpp=10&nil_src=tistory&p=1&f=section&SA=tistory&q="
naver_blog_url = "https://section.blog.naver.com/Search/Post.naver?pageNo=1&rangeType=ALL&orderBy=sim&keyword="
delay = 3 # seconds

# PC 검생량, 모바일 검색량, 총조회수
def search_amount(keyword):
  r = requests.get(f"{BASE_URL}{uri}?hintKeywords={keyword}&showDetail=1",
    headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))

  print(r.json()["keywordList"][0])
  keyword_dict = r.json()["keywordList"][0]
  return {
    "pc_serach": keyword_dict["monthlyPcQcCnt"],
    "mobile_serach": keyword_dict["monthlyMobileQcCnt"]
  }
# with io.open('data.txt', 'w', encoding='utf-8') as f:
# 	f.write(json.dumps(r.json(), ensure_ascii=False))

# 총 상품수
def total_items(keyword):
  naver_shopping_response = requests.get(f"{naver_shopping_url}{keyword}")
  soup = bs4.BeautifulSoup(naver_shopping_response.text, 'html.parser')
  search_tab = soup.find_all(attrs={"data-testid": "SEARCH_TAB_FILTER"})
  total = search_tab[0].find('span').string
  print(total)
  return total

# 총 문서수 - 다음
def total_blogs(keyword):
  daum_blog_response = requests.get(f"{daum_blog_url}{keyword}")
  soup = bs4.BeautifulSoup(daum_blog_response.text, 'html.parser')
  txt_info = soup.find('span', class_="txt_info").string
  print(txt_info)
  #총 문서수 - 네이버
  chrome_options = Options()
  # chrome_options.add_experimental_option("detach", True)
  chrome_options.add_argument('headless');
  browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
  # browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
  browser.get(f"{naver_blog_url}{keyword}")
  myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'search_number')))
  soup = bs4.BeautifulSoup(browser.page_source, 'html.parser')
  search_number = soup.find('em', class_="search_number").string
  print(search_number)
  return {
    "daum": txt_info,
    "naver": search_number
  }

# 블로그 글 가져올 링크
# https://search.naver.com/search.naver?query=%EC%A2%85%EC%9D%B4%EB%B9%A8%EB%8C%80&nso=&where=blog&sm=tab_opt