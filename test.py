# -*- coding: utf-8 -*-

from selenium import webdriver

import actives

# driver = webdriver.Chrome()
# driver.implicitly_wait(30)  # 隐性等待，最长等30秒
# screenStorePath = 'D:\\'
# URL = 'http://dev.yuceyi.com:8899/auth/login'

import fileinput

count = 0
fw = open("D:\\test4.txt", 'w')
print >> fw, "{\n\t\"system\": \"PO\",\n\t\"sku_link_list\": ["
for line in fileinput.input("D:\\tt.txt"):
    count = count + 1
    print >> fw, "{\n\"id\": %s,\n\"link_id\": 520000,\n\"sku_id\": 2510000,\n\"price\": 12.0, \n\"score\": -10, \n\"active\": true, \n\"is_default\": true \n}," % line
print >> fw, "\t]\n}"
print count
# print >> fw, "{\n\t\"system\": \"PO\",\n\t\"sku_link_list\": ["
# for i in range(1000, 2000):
#     print >> fw, "{\n\"link_id\": 52%s,\n\"sku_id\": 251%s,\n\"price\": 12.0, \n\"score\": -20, \n\"active\": true, \n\"is_default\": true \n}," % (i, i)
#     # print >> fw, "\t\t{\n\"syn_id\": \"调ddd\",\n\"url\": \"http://test1%s\",\n\"supplier_id\": 9998,\n\"score\": 24,\n\"price\":11,\n\"trade_count\": \">12\",\n\"sale_count\": 10,\n\"active\": false,\n\"sku_list\":[" % i
#     # for k in range(1430, 1439):
#     #     print >> fw, "{\n\"sku_id\": %s,\n\"price\": 3.0,\n\"score\": 4,\n\"active\": true,\n\"is_default\": false\n}," % k
#     # print >> fw, "{\n\"sku_id\": 1439,\n\"price\": 3.0,\n\"score\": 4,\n\"active\": true,\n\"is_default\": false\n}"
#     # print >> fw, "]\n},"
# #     print >> fw, "\t\t{\n\t\t\"syn_id\": \"sdfsd\",\n\t\t\"type\": 1,\n\t\t\"name\": \"义乌市普霞日用百货商行testz3000%s\",\n\t\t\"platform\": \"1688\",\n\t\t\"home_url\": \"http://shop1429289399849.1688.com\",\n\t\t\"detail_address\": \"详细地址\",\n\t\t\"warehouse_location\": \"浙江/杭州\",\n\t\t\"sale_rate\": 0.90,\n\t\t\"cooperate\": false,\n\t\t\"score\":0\n\t\t}," % i
# print >> fw, "\t]\n}"



fw.close()
