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

#f = Factory.create()
LoginUrl = "https://sso.cisco.com/autho/login/loginaction.html"
ContractManagerUrl = 'https://apps.cisco.com/CustAdv/ServiceSales/contract/viewContractMgr.do?method=viewContractMgr'

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Connection': 'keep-alive',
    'Host': 'apps.cisco.com',
    'User-Agent': 'Mozilla/5.0 (compatible; MSIE 6.0; Windows CE; Trident/4.1)',
    "Upgrade-Insecure-Requests": 1,
    'Origin':'https://apps.cisco.com',
}
formdata = {
    'userid': 'wangyang',
    'password': 'p@ssW0RD88',
    # 'target':'',
    # 'smauthreason':'',
    # 'smquerydata':'',
    # 'smagentname':'',
    # 'postpreservationdata':'',
    # 'SMENC':'',
    # 'SMLOCALE':'',
    # 'source': 'index_nav',
    # 'Referer': 'https://apps.cisco.com/CustAdv/ServiceSales/contract/viewContractMgr.do?method=viewContractMgr',
}
data = urllib.urlencode(formdata)
filename = 'cookie.txt'
cookie = cookielib.MozillaCookieJar(filename)
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
urllib2.install_opener(opener)

def parse_summit(html):

    tree = etree.HTML(html)
    # html = etree.tostring(tree) 字符串化
    # html = etree.parse(tree) 从文件读出来的需要parse
    result = tree.xpath('//title[1]/text()')
    # print "====summit title [%s]"%result
    print "===start parse_summit [%s]" % result
def contractgohtml(ContractGoHtml):
    tree = etree.HTML(ContractGoHtml)
    title = tree.xpath('//title[1]/text()')
    print "-----contractgohtml----[%s]" % title
    seqId = tree.xpath('//*[@id="seqId"]/@value')[0]
    ServiceLineId = tree.xpath('//*[@id="ServiceLineId"]/@value')[0]
    ContractNumber = tree.xpath('//*[@id="ContractNumber"]/@value')[0]
    # print "0000000000---%s" % (ContractNumber)
    formdata_b = {
        'seqId': seqId,
        'PageId': '2',
        'page': 'CS',
        'ContractNumber': ContractNumber,
        'ServiceLineId': ServiceLineId,
        'ContractType': 'HW',
        'selProdType': 'MAJOR',
        'EQT': '',
        'userType': '',
        'downloadMethod': 'SAVE',
        'Config': 'MINOR',
        'emailTo': 'service@nantian.com.cn',
        'emailCC': '',
    }
    # print "设置完参数等待下载", str(ContractNumber), str(ServiceLineId), str(seqId)
    # 提交新的formdata,请求真正的URL，action是下载
    SummitUrl = "https://apps.cisco.com/CustAdv/ServiceSales/contract/downloadContractSelectedData.do?methodName=onSubmitDataForm"
    print "===form_b: %s" % formdata_b
    data = urllib.urlencode(formdata_b)
    # headers['Referer'] = ContractGoHtml

    request = urllib2.Request(SummitUrl, data, headers)
    # 这个是真正的发出请求
    response = urllib2.urlopen(request)
    # response = opener.open(request)
    # print response
    # print response.status_code
    # 这个位置urllib2自动解决redict的问题不用手动
    fp = response.read()
    print fp
    with open(r'/Users/yu/Desktop/tutorial/spider_data/' + ContractNumber + '.zip', 'wb') as code:
        code.write(fp)


def click_go(ContractManagerHtml):
    # print "模拟点击GO"
    tree = etree.HTML(ContractManagerHtml)
    title = tree.xpath('//title[1]/text()')
    print "-----click_go----[%s]" % title
    script_text = tree.xpath('//*[@id="mod_1"]/script')[0].text
    # print script_text
    url_half = re.compile(
        'case\s\'Download Contract or Selected Data\':[\s|\S]*?url = checkBrowser\(\'(.*?)\'\);').findall(
        script_text)[0]
    # print url_half
    # print type(url_half)
    contractgourl = 'https://apps.cisco.com/CustAdv/ServiceSales/contract/' + url_half
    res = opener.open(contractgourl)
    html = res.read()
    contractgohtml(html)


def get_per_item(item):
    if item.xpath('td[2]/a/@href'):
        value = item.xpath('td[2]/a/@href')[0][1:]
        contracturl = 'https://apps.cisco.com/CustAdv/ServiceSales/contract' + value
        ContractManagerHtml = opener.open(contracturl).read()
        click_go(ContractManagerHtml)
        pass
    else:
        print "====get td error!====="


def for_each_item(items):
    print "----for each items---"
    #get_per_item(items[0])
    for item in items:
        get_per_item(item)


def get_per_page(pageurl):

    ContractPageManagerHtml = opener.open(pageurl).read()
    tree = etree.HTML(ContractPageManagerHtml)
    items = tree.xpath('//*[@id="cmDataDiv"]/table/tbody/tr')
    for_each_item(items)

def for_each_pages(pages,tableID,contextID):
    for page in range(pages):
        print "before page is [%s]" % page
        page =page + 1
        pageurl = r'https://apps.cisco.com/CustAdv/ServiceSales/contract/performTableActions.do?sortID=contractNumber&pageID=' + str(
            page) + '&tableID=' + tableID + '&contextID=' + contextID + '&method=paginateContracts&cmToLine=undefined&selectedProductsCHR=&currentPageId=1'
        # print pageurl
        print "====per page [%s]===="%page
        get_per_page(pageurl)
        # print "in page %s" % page


def getmgr():
    text = opener.open(ContractManagerUrl).read()
    # ---------------***********************************——————————————————
    # 转化成html
    tree = etree.HTML(text)
    # html = etree.tostring(tree) 字符串化
    # html = etree.parse(tree) 从文件读出来的需要parse
    result = tree.xpath('//title[1]/text()')
    print "title: %s" % result
    tableID = tree.xpath('//*[@id = "tableIdForActions"]/@value')[0]
    contextID = tree.xpath('//*[@id = "cmContextForActions"]/@value')[0]
    pages = tree.xpath('//*[@id = "mod_2"]/table/tbody/tr/td[2]')
    # //*[@id="mod_2"]/table/tbody/tr/td[2]
    print tableID
    print contextID
    print pages
    pages = 1
    for_each_pages(pages,tableID,contextID)

# class CiscoSpider():
def login():
    print "will login"
    request = urllib2.Request(LoginUrl,data,headers)
    # 这个是真正的发出请求
    response = opener.open(request)
    # 保存cookie到cookie.txt中
    cookie.save(ignore_discard=True, ignore_expires=True)
    print "login success"

# def unzip():
#
#     file_list = os.listdir(r'/Users/yu/Desktop/tutorial/spider_data/')
#
#     for file_name in file_list:
#         if os.path.splitext(file_name)[1] == '.zip':
#             print file_name
#
#             file_zip = zipfile.ZipFile(file_name, 'r')
#             for file in file_zip.namelist():
#                 file_zip.extract(file, r'.')
#             file_zip.close()
#             os.remove(file_name)
#     pass


def main():
    #setp1: login
    login()
    # 登陆合同管理
    # step:2 get mgr
    getmgr()
    #test_get_down_url()

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