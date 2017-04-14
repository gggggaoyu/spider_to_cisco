# coding:utf-8

from faker import Factory
import urllib2
import urllib
from lxml import etree
import cookielib
import re
import requests
import httplib

f = Factory.create()

class SpiderCisco(object):
    #login_url = "https://sso.cisco.com/autho/forms/CDClogin.html#"
    LoginUrl = "https://sso.cisco.com/autho/login/loginaction.html"
    ContractManagerUrl = 'https://apps.cisco.com/CustAdv/ServiceSales/contract/viewContractMgr.do?method=viewContractMgr'

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'keep-alive',
        'Host': 'sso.cisco.com',
        'User-Agent': f.user_agent(),
        "Upgrade-Insecure-Requests": 1
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
        #'Referer': 'https://apps.cisco.com/CustAdv/ServiceSales/contract/viewContractMgr.do?method=viewContractMgr',
    }
    ContractPageUrls = []
    ContractUrls = []
    ContractGoUrls = []
    DownloadSelectUrls = []

    data = urllib.urlencode(formdata)

    filename = 'cookie.txt'
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
                    'PageId': 2,
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
                headers['cookies'] = cookie
                headers['Referer'] = contractgourl
                print cookie
                data = urllib.urlencode(formdata_b)
                print 80*'()'
                print summiturl
                # r = requests.post(summiturl, data=data, headers=res.headers,cookies = cookie)
                # print dir(r)
                # print r.__dict__
                # print 80 * '@'
                print "kankan"
                # print r.status_code
                conn = httplib.HTTPConnection("sso.cisco.com")
                conn.request(method="POST", url=summiturl, body=data, headers=headers)
                response = conn.getresponse()
                print conn.__dict__
                # ress = response.getheader('location')
                # print dir(response)
                # print ress
                #print ress.__getattribute__

                # print r.text
                # k = requests.get(r.url,headers=r.request.headers,cookies = cookie)
                # print k.content
    # print r.status_code
    # print r.content
    # # r = requests.get(response.url, headers=response.request.headers)
    # print dir(r)
    #print "=====ContractNumber:%s" % ContractNumber
                # print self.flags
                # with open(r'e:' + str(self.flags) + '.zip', 'wb') as code:
                #     code.write(r.content)
    #             r = requests.get(response.url, headers=response.request.headers)
    #             #tree = etree.HTML(ishtml)
    # print ishtml







    #for page in range(1):

