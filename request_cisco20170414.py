# coding:utf-8

#from faker import Factory
import urllib2
import urllib
from lxml import etree
import cookielib
import re
import requests
import httplib

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
        page = page+2

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


def test_get_down_url():
    url = "https://apps.cisco.com/CustAdv/ServiceSales/contract/downloadContractSelectedData.do?methodName=onSubmitDataForm"
    form_eg = {
        "seqId": '221739196',
        "PageId": "2",
        "page": "CS",
        "ContractNumber": '200235624',
        "ServiceLineId": '120089445252',
        # ContractNumber:200235624
        # ServiceLineId:120089445252
        "ContractType": "HW",
        "selProdType": "MAJOR",
        "EQT":"",
        "userType":"",
        "downloadMethod":"SAVE",
        "Config":"MINOR",
        "emailTo":"service @ nantian.com.cn",
        "emailCC":""
    }
    resheaders = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'keep-alive',
        'Host': 'apps.cisco.com',
        'User-Agent': 'Mozilla/5.0 (compatible; MSIE 6.0; Windows CE; Trident/4.1)',
        "Upgrade-Insecure-Requests": 1,
        'Origin': 'https://apps.cisco.com',
        #'Referer':'https://apps.cisco.com/CustAdv/ServiceSales/contract/downloadContractSelectedData.do?methodName=onshowDownloadCSDPopup&TableID=0.404073331436679&cmContext=0.4202708969983503&sequenceID=46738755&TableIDService=0.21409383580484087&seqId=221739196'
    }


    data = urllib.urlencode(form_eg)
    request = urllib2.Request(url, data, resheaders)
    # 这个是真正的发出请求
    response = urllib2.urlopen(request)
    # response = opener.open(request)
    print response
    # print response.status_code
    # 这个位置urllib2自动解决redict的问题不用手动
    fp = response.read()
    print fp
    # with open(r'e:' + ContractNumber + '.zip', 'wb') as code:
    #     code.write(fp)


def main():
    #setp1: login
    login()
    # 登陆合同管理
    # step:2 get mgr
    getmgr()
    #test_get_down_url()


def test():
    #login_url = "https://sso.cisco.com/autho/forms/CDClogin.html#"
    ContractPageUrls = []
    ContractUrls = []
    ContractGoUrls = []
    DownloadSelectUrls = []

    data = urllib.urlencode(formdata)


    # 声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
    cookie = cookielib.MozillaCookieJar(filename)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    #
    request = urllib2.Request(LoginUrl,data,headers)
    # 这个是真正的发出请求
    response = opener.open(request)
    # 保存cookie到cookie.txt中
    cookie.save(ignore_discard=True, ignore_expires=True)
    # 利用cookie请求访问另一个网址
    text = opener.open(ContractManagerUrl).read()

# ---------------***********************************——————————————————
    # 转化成html
    tree = etree.HTML(text)
    # html = etree.tostring(tree) 字符串化
    # html = etree.parse(tree) 从文件读出来的需要parse
    result = tree.xpath('//title[1]/text()')
    print result
    tableID = tree.xpath('//*[@id = "tableIdForActions"]/@value')[0]
    contextID = tree.xpath('//*[@id = "cmContextForActions"]/@value')[0]
    pages = tree.xpath('//*[@id = "mod_2"]/table/tbody/tr/td[2]')
    # //*[@id="mod_2"]/table/tbody/tr/td[2]
    print tableID
    print contextID
    print pages

    for page in range(1):
        pageurl = r'https://apps.cisco.com/CustAdv/ServiceSales/contract/performTableActions.do?sortID=contractNumber&pageID=' + str(
            page + 1) + '&tableID=' + tableID + '&contextID=' + contextID + '&method=paginateContracts&cmToLine=undefined&selectedProductsCHR=&currentPageId=1'
        print pageurl
        ContractPageUrls.append(pageurl)
        ContractPageManagerHtml = opener.open(pageurl).read()
        tree = etree.HTML(ContractPageManagerHtml)
        items = tree.xpath('//*[@id="cmDataDiv"]/table/tbody/tr')
        print items
        print len(items)
        rlist = []
        for item in items:
            if item.xpath('td[2]/a/@href'):
                value_test = item.xpath('td[2]/a/@href')[0]
                #print value_test
                value = item.xpath('td[2]/a/@href')[0][1:]
                # print "访问合同管理中心"
                contracturl = 'https://apps.cisco.com/CustAdv/ServiceSales/contract' + value
                ContractUrls.append(contracturl)
                ContractManagerHtml = opener.open(contracturl).read()
                # print "模拟点击GO"
                tree = etree.HTML(ContractManagerHtml)
                script_text = tree.xpath('//*[@id="mod_1"]/script')[0].text
                #print script_text
                url_half = re.compile(
                    'case\s\'Download Contract or Selected Data\':[\s|\S]*?url = checkBrowser\(\'(.*?)\'\);').findall(
                    script_text)[0]
                # print url_half
                # print type(url_half)
                contractgourl = 'https://apps.cisco.com/CustAdv/ServiceSales/contract/' + url_half
                print contractgourl
                ContractGoUrls.append(contractgourl)
                res = opener.open(contractgourl)
                ContractGoHtml = res.read()
                tree = etree.HTML(ContractGoHtml)

                seqId = tree.xpath('//*[@id="seqId"]/@value')[0]
                ServiceLineId = tree.xpath('//*[@id="ServiceLineId"]/@value')[0]
                ContractNumber = tree.xpath('//*[@id="ContractNumber"]/@value')[0]
                #print "0000000000---%s" % (ContractNumber)
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
                    'emailTo': 'service @ nantian.com.cn',
                    'emailCC': '',
                }
                # print "设置完参数等待下载", str(ContractNumber), str(ServiceLineId), str(seqId)
                # 提交新的formdata,请求真正的URL，action是下载
                summiturl = 'https://apps.cisco.com/CustAdv/ServiceSales/contract/downloadContractSelectedData.do?methodName=onSubmitDataForm'
                # ishtml = opener.open(summiturl,formdata_b).read()
                # print res.headers
                # 创建MozillaCookieJar实例对象
                cookie = cookielib.MozillaCookieJar()
                # 从文件中读取cookie内容到变量
                cookie.load('cookie.txt',ignore_discard=True, ignore_expires=True)
                # 创建请求的request
                # headers['Cookies'] = cookie
                # headers['Referer'] = contractgourl
                print cookie
                data = urllib.urlencode(formdata_b)
                print 80*'()'
                print summiturl
                r = requests.post(summiturl, data=data, headers=res.headers,cookies = cookie)
                # r1 = requests.get(summiturl,headers=res.headers, cookies=cookie)
                print dir(r)
                print r.__dict__
                print 80 * '@'
                print "kankan"
                print r.status_code
                print r.content

if __name__ == "__main__":
    main()