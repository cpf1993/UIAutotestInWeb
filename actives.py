# -*- coding: utf-8 -*-
import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import time
import requests
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# create a file handler
handler = logging.FileHandler('UIAutomationLogs.log')
handler.setLevel(logging.INFO)
# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(handler)


# Login
def login_with(driver, _username, _password):
    try:
        driver.find_element_by_name('username').send_keys(_username)
        driver.find_element_by_name('password').send_keys(_password)
        driver.find_element_by_xpath('//*[@id="login-form"]/button').click()
        return True
    except NoSuchElementException as e:
        # logger.info(e.message)
        logger.info(e.message)
        return False


# Logout
def logout(driver):
    try:
        time.sleep(3)
        driver.find_element_by_id("logout_link").click()
        return True
    except NoSuchElementException as e:
        logger.info(e.message)
        return False


# 截图用作结果比较，未做长截图，用当前页面的title作为文件名
def save_screenshot(driver, my_path):
    time.sleep(1)
    if not os.path.exists(my_path):
        os.makedirs(my_path)
    titleName = modify_title_to_filename(driver.title)
    try:
        driver.get_screenshot_as_file(my_path + titleName[0:20] + '.png')
        return True
    except NoSuchElementException as e:
        logger.info(e.message)
        return False


# 截图用作结果比较，未做长截图，自定义文件名
def save_screenshot_with_name(driver, my_path, filename):
    time.sleep(1)
    if not os.path.exists(my_path):
        os.makedirs(my_path)
    titleName = modify_title_to_filename(filename)
    try:
        driver.get_screenshot_as_file(my_path + titleName + '.png')
        return True
    except NoSuchElementException as e:
        logger.info(e.message)
        return False


# 修正不正确的文件名
def modify_title_to_filename(title_name):
    invalid_Symbols = '\/*?"<>:|'
    for c in title_name:
        if c in invalid_Symbols:
            title_name = title_name.replace(c, '')
        if c == ' ':
            title_name = title_name.replace(c, '_')
    return title_name


# 下拉框操作，使用select_by_value(value)
def select_to(selector, to_element):
    # To-do, element比较多的时候控制滚屏
    try:
        Select(selector).select_by_value(to_element)
        return True
    except Exception as e:
        logger.info(e.message)
        return False


# 下拉框操作，使用select_by_visible_text(text)
def select_to_bytext(selector, to_element):
    try:
        Select(selector).select_by_visible_text(to_element)
        return True
    except Exception as e:
        logger.info(e.message)
        return False


# 对radio复选框进行操作,可以通过发送空格的方式达到选中或者反选的目的
def click_radio(driver, element_list):
    _xpath = "//input[@value='%s' and @type='radio']" % element_list
    try:
        myRadio = driver.find_element_by_xpath(_xpath)
    except NoSuchElementException as e:
        logger.info(e.message)
        return False
    if not myRadio.is_selected():
        # myRadio.click()
        myRadio.send_keys(Keys.SPACE)
    return True


# 对checkbox复选框进行操作
def click_checkbox(driver, elementlist):
    # 如果假如参数“All”就全部勾选
    if elementlist == 'All':
        try:
            elements = driver.find_elements_by_xpath("//input[@type='checkbox']")
        except NoSuchElementException as e:
            logger.info(e.message)
            return False

        for element in elements:
            if not element.is_selected():
                element.click()
        return True

    # 再判断是不是单独一个String，即想选的框
    if type(elementlist) == basestring:
        _xpath = "//input[@value='%s' and @type='checkbox']" % elementlist
        try:
            myCheckBox = driver.find_element_by_xpath(_xpath)
            if not myCheckBox.is_selected():
                myCheckBox.click()
        except NoSuchElementException as e:
            logger.info(e.message)
            return False
    elif type(elementlist) == list:
        # 不然我们就提供一个list，按照value选择
        for element in elementlist:
            _xpath = "//input[@value='%s' and @type='checkbox']" % element
            try:
                myCheckBox = driver.find_element_by_xpath(_xpath)
                if not myCheckBox.is_selected():
                    myCheckBox.click()
            except NoSuchElementException as e:
                logger.info(e.message)
                return False
    else:
        print 'Wrong Parameters!'
        return True


# 简单的检索
# input： driver 当然是webdriver
#        where 搜索框内文字提示的一部分
#        what 想要进行检索的内容
def retrieve(driver, where, what):
    _xpath = "// input[contains(@placeholder, '%s')]" % where
    try:
        driver.find_element_by_xpath(_xpath).send_keys(what)
        click_button(driver, '检索')
        return True
    except NoSuchElementException as e:
        logger.info(e.message)
        return False


# 因为检索按钮在称重页面有多个 此方法只输入检索内容 不点击检索按钮
def retrieve_only(driver, where, what):
    _xpath = "// input[contains(@placeholder, '%s')]" % where
    try:
        driver.find_element_by_xpath(_xpath).send_keys(what)
        return True
    except NoSuchElementException as e:
        logger.info(e.message)
        return False


# 只是为了更简单地按button
def click_button(driver, button_name):
    _xpath = "//button[text()='%s']" % button_name
    locator = (By.XPATH, _xpath)
    WebDriverWait(driver, 5, 0.5).until(EC.visibility_of_element_located(locator))
    try:
        driver.find_element_by_xpath(_xpath).click()
        return True
    except NoSuchElementException as e:
        logger.info(e.message)
        return False


# 类似于存在多个“编辑”按钮时，可以使用该函数,选择点击第几个“编辑”按钮，the_one指的是第几个按钮
def click_button_smart(driver, button_name, the_one):
    _xpath = "//button[text()='%s']" % button_name
    locator = (By.XPATH, _xpath)
    WebDriverWait(driver, 5, 0.5).until(EC.visibility_of_all_elements_located(locator))
    try:
        driver.find_elements_by_xpath(_xpath)[the_one - 1].click()
        return True
    except NoSuchElementException as e:
        logger.info(e.message)
        return False


# 通過className定位按鈕
def click_button_by_class(driver, class_name, the_one):
    _xpath = "//*[contains(@class,'%s')]" % class_name
    locator = (By.XPATH, _xpath)
    WebDriverWait(driver, 5, 0.5).until(EC.visibility_of_all_elements_located(locator))
    try:
        driver.find_elements_by_xpath(_xpath)[the_one - 1].click()
        return True
    except NoSuchElementException as e:
        logger.info(e.message)
        return False


# 只适合在采购系统里面进行搜索
# title：搜索框标题，精确匹配
# _input：要搜索的内容
def search_in_purchase(driver, title, _input):
    _xpath = "//div[text()='%s']/following-sibling::div[2]/input" % title
    try:
        driver.find_element_by_xpath(_xpath).send_keys(_input)
        driver.find_element_by_xpath(_xpath).send_keys(Keys.ENTER)
        return True
    except NoSuchElementException as e:
        logger.info(e.message)
        return False


# 只适合在订单系统里面进行搜索
# title：搜索框标题，精确匹配
# _input：要搜索的内容
def search_in_sale_order(driver, title, _input):
    _xpath = "//span[text()='%s']/following-sibling::input[1]" % title
    try:
        driver.find_element_by_xpath(_xpath).send_keys(_input)
        driver.find_element_by_xpath(_xpath).send_keys(Keys.ENTER)
        return True
    except NoSuchElementException as e:
        logger.info(e.message)
        return False


def input_in_purchase(driver, _input):
    _xpath1 = "//a[@data-name='external_order_id']"
    _xpath2 = "//input[@class='form-control input-sm']"
    try:
        driver.find_element_by_xpath(_xpath1).click()
        driver.find_element_by_xpath(_xpath2).clear()
        driver.find_element_by_xpath(_xpath2).send_keys(_input)
        driver.find_element_by_xpath(_xpath2).send_keys(Keys.ENTER)
        #        driver.find_element_by_xpath(_xpath1).send_keys(Keys.ARROW_RIGHT)
        return True
    except NoSuchElementException as e:
        logger.info(e.message)
        return False


# 作用很有限，仅仅在采购页面临时使用，以后用更好的方法替代
def scroll_to_right(driver, times):
    _xpath1 = "//a[@data-name='external_order_id']"
    for i in range(0, times):
        try:
            driver.find_element_by_xpath(_xpath1).send_keys(Keys.ARROW_RIGHT)
        except NoSuchElementException as e:
            logger.info(e.message)
            return False
    return True


def click_by_text(driver, link_text):
    try:
        driver.find_element_by_link_text(link_text).click()
        return True
    except NoSuchElementException as e:
        logger.info(e.message)
        return False


# 只是为了普通的点击
def click_ordinary(driver, the_path):
    try:
        driver.find_element_by_xpath(the_path).click()
        return True
    except NoSuchElementException as e:
        logger.info(e.message)
        return False


# 对于普通的输入框，使用xpath定位元素，方便输入文本my_input
def input_ordinary(driver, the_xpath, my_input):
    try:
        driver.find_element_by_xpath(the_xpath).send_keys(my_input)
        return True
    except NoSuchElementException as e:
        logger.info(e.message)
        return False


# 对于普通的输入框，在输入前，将已有的数据删除
def clear_ordinary(driver, the_xpath):
    try:
        driver.find_element_by_xpath(the_xpath).clear()
        return True
    except NoSuchElementException as e:
        logger.info(e.message)
        return False


# 对于某些使用clear()无法清除的输入框，模拟键盘和鼠标操作，清除已有数据
def clear_special(driver, the_xpath):
    use_mouse = driver.find_element_by_xpath(the_xpath)
    try:
        driver.find_element_by_xpath(the_xpath).send_keys(Keys.CONTROL, 'a')
        driver.find_element_by_xpath(the_xpath).send_keys(Keys.BACK_SPACE)
        return True
    except NoSuchElementException as e:
        logger.info(e.message)
        return False


# 通过发request的方式来跑某些接口，这个函数用于入库确认。
# order_or_idle 决定是闲置库位还是订单库位，1是闲置，其他是订单
def stock_in_by_requests(sku_no, box_name, numbers, order_or_idle):
    _headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Ilx1NWYwMFx1NTNkMVx1ODAwNSIsImlzX2Nvb3BlcmF0aXZlX3N1cHBsaWVyIjp0cnVlLCJsb2dpbl9uYW1lIjoiZGV2ZWxvcGVyIiwiZXhwIjoxNTE1NDY1NDE1LCJ1c2VyX2lkIjoxLCJ1c2VyX3V1aWQiOiJTVVA2NzQ3NTk4NTciLCJlbWFpbCI6IiJ9.HXJ4SrnGbYgITZpJcOQ4A8_MluiXxIGPzKYhnU4pue4"
    }
    if order_or_idle:
        _url = "http://dev.yuceyi.com:5678/wms/pda/batch_operate/shelve"
        _body = {
            "box_name": box_name,
            "sku_id": sku_no,
            "sku_qty": numbers
        }
        try:
            requests.patch(url=_url, data=_body, headers=_headers)
            return True
        except Exception as e:
            logger.info(e.message)
            return False
    else:
        _url = "http://dev.yuceyi.com:5678/wms/pda/operate/shelve"
        _body = {
            "box_name": box_name,
            "sku_id": sku_no
        }
        for i in range(numbers):
            try:
                requests.patch(url=_url, data=_body, headers=_headers)
            except Exception as e:
                logger.info(e.message)
                return False
        return True


# 捕获web toast并返回其文本信息，用于断言
# alert_class: alert toast alert-success, alert toast alert-info, alert toast alert-danger
def catch_web_toast(driver, alert_class):
    _xpath = "//div[@class='%s']" % alert_class
    locator = (By.XPATH, _xpath)
    # locator = (By.CLASS_NAME, 'alert toast alert-info')
    try:
        WebDriverWait(driver, 5, 0.1).until(EC.visibility_of_element_located(locator))
        return driver.find_element_by_xpath(_xpath).text
    except Exception as e:
        logger.info(e.message)
        return ""


# 用js方法来向日历控件里面写值
def send_keys_into_calendar(driver, locator, value):
    # 去掉元素的readonly属性
    js = 'document.getElementBy' + locator[0] + '("' + locator[1] + '").removeAttribute("readonly");'
    driver.execute_script(js)
    # 用js方法输入日期
    js_value = 'document.getElementBy' + locator[0] + '("' + locator[1] + '").value="' + value + '"'
    driver.execute_script(js_value)
    return


# 判断元素是否存在
# element_name 元素，如div,span,button
# css_selector选择器类型，如class,name,id等
# value选择器标识值，class,name,id对应值
# the_one 第几个符合条件的元素
def is_ele_exist(driver, element_name, css_selector, value, the_one):
    _xpath = "// %s[%s][%s ='%s']" % (element_name, the_one-1, css_selector, value)
    locator = (By.XPATH, _xpath)
    try:
        WebDriverWait(driver, 5, 0.5).until(EC.visibility_of_all_elements_located(locator))
        return True
    except Exception as e:
        logger.info(e.message)
        return False
