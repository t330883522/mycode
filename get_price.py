# 获取单个基金的历史数据
# 获取多个基金的历史数据
# 存储到数据库
# 获取所有货币基金的数据
# 增加多进程
# 数据比较大，时间比较长
from multiprocessing.pool import Pool

import time
from pyquery import PyQuery as pq
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pymongo

# codes = ['161725', '160222', '000248']
codes = ['161725', '160222', '000248', '160632', '481012', '165312', '164906', '530015', '217027', '540012', '110003',
             '001631', '001632', '167301', '320010', '310398', '000835', '164508', '070023', '519671', '213010', '410008',
             '163808', '240014', '519706', '530018', '000311', '217016', '502020', '160628', '519100', '163407', '000312',
             '001586', '160716', '502040', '001587', '162307', '003876', '000313', '162714', '162509', '501021', '001237',
             '001548', '001549', '162213', '100038', '399001', '502048', '110030', '050021', '000176', '161714', '240016',
             '240019', '003261', '001051', '180003', '003262', '110019', '002315', '167601', '002310', '501050', '050002',
             '001458', '161207', '002976', '530010', '090010', '161607', '161211', '161604', '160121', '166802', '519116',
             '165515', '161812', '200002', '160615', '160417', '000071', '000948', '161721', '217017', '000950', '165309',
             '164811', '202015', '001469', '160218', '164705', '165806', '160517', '161227', '002979', '020021', '519931',
             '660008', '110020', '000051', '160814', '020011', '270010', '160706', '100032', '000368', '481009', '000961',
             '001015', '002588', '002987', '519027', '700002', '001539', '161811', '370023', '000042', '161128', '001016',
             '161213', '040002', '166007', '161723', '001594', '519686', '001595', '460300', '003986', '000613', '310318',
             '161121', '165519', '160213', '003579', '270042', '161127', '118002', '161507', '050013', '160807', '040180',
             '519180', '003015', '161831', '519300', '160418', '110031', '165520', '161907', '501025', '040046', '161029',
             '003475', '160717', '168205', '001588', '161217', '740101', '000975', '001589', '160631', '000834', '165521',
             '163116', '160224', '160806', '000373', '690008', '161118', '502006', '000376', '160809', '050024', '450008',
             '001552', '501023', '001553', '163111', '001617', '160136', '206005', '001618', '160516', '000656', '001420',
             '180033', '257060', '160137', '160922', '001426', '161816', '233010', '202021', '161819', '470068', '161026',
             '160625', '040190', '161612', '002316', '160219', '163118', '217019', '001242', '000614', '160620', '002311',
             '501009', '501010', '502013', '161126', '160415', '519034', '002906', '160635', '519032', '502023', '000968',
             '090012', '470007', '001397', '160626', '002907', '161715', '162216', '202017', '002982', '110021', '162415',
             '161124', '161032', '206010', '160225', '050025', '501029', '585001', '161726', '003578', '000369', '165707',
             '161125', '163109', '168203', '003016', '161017', '001092', '410010', '160221', '460220', '001180', '100053',
             '168204', '161724', '002978', '001460', '519981', '001459', '096001', '002973', '270026', '002975', '001713',
             '161122', '000049', '163821', '290010', '161033', '168001', '001133', '160808', '001361', '002977', '001027',
             '001554', '001550', '161825', '002510', '502000', '001555', '001551', '165511', '160636', '160616', '000478',
             '270027', '263001', '519117', '320014', '162010', '162907', '202025', '519677', '001214', '160638', '160634',
             '164401', '001629', '001630', '168201', '001241', '001560', '502016', '160640', '001561', '164821', '150152',
             '003646', '161025', '003647', '001455', '000059', '167503', '003194', '000008', '000962', '001052', '160119',
             '162711', '001599', '501011', '162510', '002903', '001600', '001899', '000942', '501012', '002974', '502010',
             '510080', '164809', '161028', '202211', '003079', '163114', '660011', '001064', '000218', '002610', '001351',
             '000307', '164905', '002984', '003083', '000216', '003080', '161223', '003085', '003081', '002611', '501005',
             '002963', '000217', '003086', '003084', '003082', '001113', '161119', '003366', '161120', '002900', '167701',
             '001590', '160416', '163119', '165809', '001591', '161826', '163209', '161718', '160633', '000022', '000023',
             '161910', '502056', '164304', '164819', '161027', '590007', '165523', '163113', '160720', '160123', '001021',
             '160721', '502053', '160419', '160124', '165522', '001023', '161031', '165315', '161720', '020036', '162412',
             '161629', '020035', '004085', '004086', '502036', '502026', '165525', '160135', '165524', '164907', '000088',
             '000087', '003376', '002656', '003358', '160639', '003377', '501002', '164908', '501007', '501008', '002236',
             '110026', '070030', '161123', '160223', '001592', '001593', '502030', '161022', '164820', '160637', '000179',
             '501031', '501030', '162413', '161613', '162411', '001611', '001612', '160629', '003017', '161628', '000596',
             '502003', '002199', '163115', '161024', '164402', '163117', '164818', '161030', '160630', '160420', '150153',
             '004346', '004347', '161631', '004243', '004195', '004191', '003548', '004190', '160422', '004070', '003318',
             '003702', '004354', '004348', '004532', '004343', '501016', '004069', '004194', '501105', '004342', '004432',
             '004533', '004643', '501020', '501302', '160138', '004593', '004642', '004597', '004433', '160139', '004253',
             '003766', '160643', '004345', '161037', '501102', '004598', '004193', '162719', '501019', '166402', '003765',
             '005112', '005063', '004996', '004857', '004192', '004344', '005062', '004855', '005563', '004752', '164823',
             '501103', '005319', '501303', '160924', '501301', '005051', '005279', '005390', '005391', '004753', '005568',
             '004854', '501101', '005320', '005567', '005564', '005566', '005555', '005554', '004856', '005224', '005223',
             '005064', '160140', '005288', '005414', '004945', '160141', '005052', '005287', '005415','005565']

MONGO_URL = 'localhost'
MONGO_DB = 'easymoney'
MONGO_TABLE = 'all_code_date_price'

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]
browser = webdriver.Firefox()
wait = WebDriverWait(browser, 10)

def get_products(code):
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#jztable > table > thead > tr > th.first')))
    html = browser.page_source
    doc = pq(html)
    items = doc('.w782 tbody tr').items()
    for item in items:
        date = item.find('td').text().split(' ')[0]
        price = item.find('.tor').text().split(' ')[0]
        product = {
            'code':code,
            'date': date,
            'price': price
        }
        save_to_mongo(product)


def save_to_mongo(result):
    try:
        if db[MONGO_TABLE].insert(result):
            pass
            # print('存储到MONGODB成功', result)
    except Exception:
        print('存储到MONGODB失败', result)

def next_page(page_number,code):
    print('正在翻页', page_number)
    try:
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#pagebar > div.pagebtns > input.pnum'))
        )
        submit = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#pagebar > div.pagebtns > input.pgo')))
        input.clear()
        input.send_keys(page_number)
        submit.click()
        wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#pagebar > div.pagebtns > input.pgo')))
        get_products(code)
    except TimeoutException:
        next_page(page_number,code)

def main():
    num = 1
    for code in codes:
        print('正在下载-----{}----代码为----{}----'.format(num,code))
        num = num+1
        # print('code',code)
        url = 'http://fund.eastmoney.com/f10/jjjz_' + code + '.html'
        try:
            browser.get(url)
            html = browser.page_source
            doc = pq(html)
            page = doc.find('.pagebtns label').text()
            page = page.split(' ')[-2]
            page = int(page)
            for i in range(1, page+1):
                next_page(i,code)
        except Exception:
            print('出错啦')

if __name__ == '__main__':
    main()


#