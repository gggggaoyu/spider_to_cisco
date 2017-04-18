# coding:utf-8

#from faker import Factory
import urllib2
import urllib
from lxml import etree
import cookielib
import re
import requests
import httplib
import zipfile
import os


def unzip():

    file_list = os.listdir(r'/Users/yu/Desktop/tutorial/spider_data/')
    #print file_list
    for file_name in file_list:
        if os.path.splitext(file_name)[1] == '.zip':
            # ('200235610', '.zip')
            print file_name
            file_zip = zipfile.ZipFile(file_name, 'r')
            print file_zip
            # for file in file_zip.namelist():
            #     file_zip.extract(file, r'/Users/yu/Desktop/tutorial/spider_data_c/')
            # file_zip.close()
            # os.remove(file_name)
    pass


def main():
    # setp1: login
    # login()
    # 登陆合同管理
    # step:2 get mgr
    # getmgr()
    #test_get_down_url()
    unzip()
    pass

if __name__ == "__main__":
    main()


#在serverdesk的服务台里写一个按钮，叫做导入思科合同
#字段包括如下eq
# SN = fields.Char(required=True,string="SERIAL NUMBER / PAK NUMBER") #序列号
#     contract = fields.Many2one('server_desk.contract', string="CONTRACT NUMBER") #合同号
#     server_level = fields.Char(string="SERVICE LEVEL") #服务级别
#     company = fields.Char(string="BILL TO NAME") #公司名称
#     customer = fields.Many2one('res.partner',string="SITE NAME" ,domain=[('category','=',u'case客户')]) #客户名称
#     product = fields.Char(string="PRODUCT NUMBER") #产品型号
#     product_relationship = fields.Char(string="PRODUCT RELATIONSHIP") #产品相互关系
#     description  = fields.Char(string="DESCRIPTION") #产品描述
#     begin_date = fields.Date(string="BEGIN DATE") #维保开始日期
#     end_date = fields.Date(string="END DATE") #维保结束日期
#     last_date_of_support = fields.Date(string="LAST DATE OF SUPPORT") #EOS日期
#     product_ship_date = fields.Date(string="PRODUCT SHIP DATE") #产品发货日期
#字段包括如下con
# contract_id = fields.Char(string="Contract Number", required=True)
#     start_time = fields.Date(compute='_count_time',store='True')
#     stop_time = fields.Date(compute='_count_time',store='True')
#     serivce_category1 = fields.Char()
#     serivce_category2 = fields.Char()
#     sow = fields.Text()
#     serivce_level = fields.Char()
#     cco = fields.Many2many('server_desk.cco_account', string="CCO")
#     bill2id = fields.Char(string="Bill To ID ")
#     contract_type = fields.Char(string="Contract Type")
#     access_level = fields.Char(string="Access Level")
#     software_download = fields.Char(string="Software Download")
#     srv_req = fields.Char(string="Service Request Management")
#     locked = fields.Char(string="Locked")
#     site_name = fields.Char(string="Installed-At Site Name ")
#     partner_id = fields.Many2many('res.partner', string="客户", domain=[('category','=',u'case客户')])
#     equipment_ids = fields.One2many('server_desk.equipment','contract',string="设备")
# CONTRACT NUMBER/SERVICE LEVEL/BILL TO NAME/SITE NAME/PRODUCT NUMBER／DESCRIPTION/BEGIN DATE/END DATE/
# LAST DATE OF SUPPORT/PRODUCT SHIP DATE／找不到产品关系
#  以上是已有字段
# CONTRACT LABEL/SERVICE LEVEL STATUS/BILL TO ADDRESS/BILL TO CITY
# BILL TO STATE/PROVINCE//BILL TO POSTAL CODE/BILL TO COUNTRY/BILL-TO CONTACT/BILL-TO PHONE/BILL-TO EMAIl/
# SITE ID/SITE ADDRESS/SITE ADDRESS LINE2/SITE ADDRESS LINE3/SITE CITY/SITE STATE / PROVINCE/SITE POSTAL CODE
# /SITE COUNTRY/SITE PARENT COMPANY NAME/SITE PARENT COMPANY ID/SITE NOTES/SITE LABEL/SITE CONTACT/SITE PHONE/SITE EMAIL
# /DISTRIBUTOR BILL TO ID/DISTRIBUTOR BILL TO NAME/PRODUCT QUANTITY//PRIORITY ITEM (GROUP S)/SERIAL NUMBER
# /PRODUCT LABEL/PRODUCT TYPE/COVERED PRODUCT STATUS/PRODUCT SO NUMBER
# /MAINTENANCE PO NUMBER/MAINTENANCE SO NUMBER/DO NOT RENEW REASON CODE/WARRANTY TYPE/WARRANTY END DATE/
# /SHIPMENT DELIVERY NOTICE
#
#