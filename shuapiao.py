# coding=utf-8

from selenium import webdriver

import actives
import time
import sys

for i in range(1, 2):
    driver = webdriver.Chrome()
    driver.implicitly_wait(30)

    URL = 'https://wj.qq.com/s2/5246455/7059/'
    driver.get(URL)
    driver.maximize_window()
    driver.implicitly_wait(2)

    xpath_1 = '//*[@id="question_q-1-2kHr"]/div[2]/input'
    xpath_2 = '//*[@id="question_q-2-HjYS"]/div[2]/input'
    xpath_3 = '//*[@id="question_q-3-cXCD"]/div[2]/input'
    xpath_4 = '//*[@id="question_q-6-o6rO"]/div[2]/input'

    actives.input_ordinary(driver, xpath_1, u"")
    actives.input_ordinary(driver, xpath_2, u"")
    actives.input_ordinary(driver, xpath_3, u"")
    actives.input_ordinary(driver, xpath_4, u"")

    button_xpath = '//*[@id="root-container"]/div/div/div[1]/div[2]/div[3]/div/button/span'
    actives.click_ordinary(driver, button_xpath)
    driver.close()
