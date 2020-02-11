# coding=utf-8

from selenium import webdriver

import actives
import time
import sys


driver = webdriver.Chrome()
driver.implicitly_wait(30)

URL = 'https://dev.yuceyi.com/auth/login'
driver.get(URL)
driver.maximize_window()
actives.login_with(driver, 'developer', '')

actives.click_by_text(driver, '供应商运营中心')

driver.implicitly_wait(30)

# 运营工具页
actives.click_ordinary(driver, "//*[@id='root']/section/aside/div/ul/li[2]/div/span/span")

# 异常处理页
actives.click_ordinary(driver, "//*[@id='/app/optool$Menu']/li/span")

# 缺货率处理
actives.click_ordinary(driver, "//*[@id='root']/section/section/main/aside/div[2]/div[1]")

# 签收率处理
# actives.click_ordinary(driver, "//*[@id='root']/section/section/main/aside/div[2]/div[2]")

time.sleep(1)

f = open(r"/Users/chenpengfei/Desktop/101条po数据.txt")
# f = open(r"/Users/chenpengfei/Desktop/101条快递单数据.txt")
lines = f.readlines()
print (lines)
po_uuid_list =lines
for po_uuid in po_uuid_list:
    # po_uuid = eval(po_uuid)
    po_uuid = po_uuid.replace('"', '')
    driver.find_element_by_xpath('//*[@id="root"]/section/section/main/aside/div[2]/div[1]/form/div/div/div/span/textarea').send_keys(po_uuid)
    # driver.find_element_by_xpath('//*[@id="root"]/section/section/main/aside/div[2]/div[1]/form/div/div/div/span/textarea').send_keys(po_uuid)