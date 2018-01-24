#获取全部指数基金代码

from pyquery import PyQuery as pq
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pymongo


MONGO_URL = 'localhost'
MONGO_DB = 'easymoney'
MONGO_TABLE = 'product_name_code'

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]


browser = webdriver.Firefox()
wait = WebDriverWait(browser, 10)
codes = []
def get_products():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#pgo_6')))
    html = browser.page_source
    doc = pq(html)
    items = doc('.mainTb tbody tr').items()
    for item in items:
        code = item(' td').text()
        codenum = code.split(' ')
        # print(codenum)
        # print()
        code = codenum[0]
        product = {
            'name': item.find('.fname').text(),
            'code': code
        }
        save_to_mongo(product)
        codes.append(code)
        print(codes)
        print(product)

def next_page(page_number):
    print('正在翻页', page_number)
    try:
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#pnum'))
        )
        submit = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#pgo_6')))
        input.clear()
        input.send_keys(page_number)
        submit.click()
        wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#pgo_6')))
        get_products()
    except TimeoutException:
        next_page(page_number)



def save_to_mongo(result):
    try:
        if db[MONGO_TABLE].insert(result):
            print('存储到MONGODB成功', result)
    except Exception:
        print('存储到MONGODB失败', result)





def main():
    try:

        browser.get('http://fundact.eastmoney.com/banner/zs.html')
        for i in range(1, 7):
            next_page(i)
    except Exception:
        print('出错啦')
    # get_products()
    finally:
        browser.close()

if __name__ == '__main__':
    main()
