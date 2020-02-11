# -*- coding: utf-8 -*-

# import sys
from selenium import webdriver

import unittest
import actives
import time
import ConfigParser

# reload(sys)
# sys.setdefaultencoding('utf-8')

driver = webdriver.Chrome()
driver.implicitly_wait(30)  # 隐性等待，最长等30秒


class UTest(unittest.TestCase):
    def setUp(self):
        config = ConfigParser.ConfigParser()
        config.read("../conf.conf")
        self.screen_store_path = config.get("purchase", "screen_store_path")
        self.URL = config.get("environment", "purchase_url")
        self.sku = config.get("purchase", "sku")

    # @unittest.skip("Pass")
    def test_confirm_open_purchase_order(self):
        # Apply URL
        driver.get(self.URL)
        driver.maximize_window()
        actives.save_screenshot(driver, self.screen_store_path)
        # Login
        actives.login_with(driver, 'developer', '123123')
        actives.save_screenshot_with_name(driver, self.screen_store_path, 'Login')
        # Add PO manually
        actives.click_by_text(driver, '采购管理 Procurement')
        actives.save_screenshot_with_name(driver, self.screen_store_path, 'Into purchase manage page')
        # prepare test data
        driver.find_element_by_id('quotation-add').click()
        actives.save_screenshot_with_name(driver, self.screen_store_path, 'New test sku data')
        actives.input_ordinary(driver, "//input[@id='add-quotation-sku']", self.sku)
        actives.save_screenshot_with_name(driver, self.screen_store_path, 'Input sku')
        actives.input_ordinary(driver, "//input[@id='add-quotation-quantity']", 1)
        actives.save_screenshot_with_name(driver, self.screen_store_path, 'Input quantity')
        driver.find_element_by_id('add-quotation-confirm').click()
        actives.save_screenshot_with_name(driver, self.screen_store_path, 'finish data set')
        # driver.find_element_by_id('quotation-add').click()
        # for sku_no in self.sku_list:
        #     driver.find_element_by_id('add-quotation-sku').send_keys(sku_no)
        #     driver.find_element_by_id('add-quotation-quantity').send_keys(5)
        # driver.find_element_by_id('add-quotation-confirm').click()
        # time.sleep(1)
        # Search some skus in open purchase order list
        actives.search_in_purchase(driver, 'sku', self.sku)
        actives.save_screenshot_with_name(driver, self.screen_store_path, '未采购列表')
        # Add third-party order number
        actives.input_in_purchase(driver, u'供应商test')
        actives.save_screenshot_with_name(driver, self.screen_store_path, 'input')
        # Scroll to right to show the confirm button
        actives.scroll_to_right(driver, 20)
        time.sleep(1)
        # driver.find_element_by_id('td-btn-298').click()
        # actives.click_button(driver, '确认')
        confirm_buttons = driver.find_elements_by_xpath("//button[text()='确认']")
        confirm_buttons[2].click()
        actives.save_screenshot_with_name(driver, self.screen_store_path, 'aaa')

        # driver.find_element_by_xpath("//button[text() = '是']").click()
        actives.click_button(driver, '是')
        actives.save_screenshot_with_name(driver, self.screen_store_path, '确认采购')
        actives.logout(driver)

    # @unittest.skip("Pass")
    def test_into_store(self):
        # Apply URL and login
        driver.get(self.URL)
        driver.maximize_window()
        actives.login_with(driver, 'developer', '123123')
        actives.click_by_text(driver, '采购管理 Procurement')
        time.sleep(3)
        actives.click_by_text(driver, '入库')
        actives.search_in_purchase(driver, 'sku', self.sku)
        actives.save_screenshot_with_name(driver, self.screen_store_path, '已采购列表')

        actives.scroll_to_right(driver, 20)
        time.sleep(3)
        driver.find_element_by_xpath("//input[@value='分配']").click()
        actives.save_screenshot_with_name(driver, self.screen_store_path, '入库分配')

        driver.find_element_by_xpath("//input[@value='获取']").click()
        time.sleep(3)
        max_store_num = driver.find_element_by_xpath("//input[@type='number']").get_attribute('value')
        box_name = driver.find_element_by_xpath("//input[@name='box_name']").get_attribute('value')
        # web_element = driver.find_element_by_xpath("//input[@type='number' and @class='form-control move_num']")
        # web_element.clear()
        # web_element.send_keys(max_store_num)
        actives.save_screenshot_with_name(driver, self.screen_store_path, '入库')
        driver.find_element_by_xpath("//input[@value='确认并打印']").click()
        print("box_name:"+box_name+","+"max_store_num:"+max_store_num)
        actives.stock_in_by_requests(self.sku, box_name, int(max_store_num), 0)

    @unittest.skip("Pass")
    def test_stock_out(self):
        # Apply URL and login
        driver.get(self.URL)
        driver.maximize_window()
        actives.login_with(driver, 'developer', '')

        actives.click_by_text(driver, u'WMS系统')
        actives.click_by_text(driver, u'出库')

        actives.click_checkbox(driver, 'All')
        actives.click_button(driver, u'计算出库单数量')

    # @unittest.skip("Pass")
    def test_cooperation_supplier_bill_management(self):
        pay_types = ['week', 'month', 'half_month']
        # Apply URL and login
        driver.get(self.URL)
        driver.maximize_window()
        actives.login_with(driver, 'developer', '123123')

        actives.click_by_text(driver, u'采购管理 Procurement')
        actives.click_by_text(driver, u'合作供应商')
        actives.click_by_text(driver, u'账单')
        actives.save_screenshot_with_name(driver, self.screen_store_path, u'合作供应商账单账户信息')

        # Search in this page
        driver.find_element_by_id('send-search-button').click()
        driver.find_element_by_xpath("//input[@name = 'supplier_name']").send_keys(u'金湖智盛服装店')
        actives.select_to(driver.find_element_by_xpath("//select[@name='bank_name']"), u'中国银行')
        actives.click_button(driver, u'搜索')
        actives.save_screenshot_with_name(driver, self.screen_store_path, u'金湖智盛服装店账户信息')

        # Switch to settlement page
        actives.click_by_text(driver, u'结算信息')
        actives.save_screenshot_with_name(driver, self.screen_store_path, u'结算信息')
        driver.find_element_by_id('send-search-button').click()
        for pay_type in pay_types:
            actives.select_to(driver.find_element_by_xpath("//select[@name='pay_type']"), pay_type)
            actives.click_button(driver, u'搜索')
            actives.save_screenshot_with_name(driver, self.screen_store_path, pay_type)

        # Switch to bill management
        actives.click_by_text(driver, u'账单管理')
        actives.save_screenshot_with_name(driver, self.screen_store_path, u'账单管理')
        driver.find_element_by_id('send-search-button').click()
        # 去掉元素的readonly属性
        js = 'document.getElementById("test").removeAttribute("readonly");'
        driver.execute_script(js)
        # 用js方法输入日期
        #        date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        #        js_value = 'document.getElementById("test").value="' + date + '"'
        js_value = 'document.getElementById("test").value="2017-11-01"'
        driver.execute_script(js_value)
        actives.click_button(driver, u'搜索')
        actives.save_screenshot_with_name(driver, self.screen_store_path, u'search with calendar')

        # Switch to requisition management
        actives.click_by_text(driver, u'请款单管理')
        actives.save_screenshot_with_name(driver, self.screen_store_path, u'请款单管理')


if __name__ == '__main__':
    unittest.main()
    suite = unittest.TestSuite()
    suite.addTest(UTest('test_confirm_open_purchase_order'))
    runner = unittest.TextTestRunner()
    runner.run(suite)

