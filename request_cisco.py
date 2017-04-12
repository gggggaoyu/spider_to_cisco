# coding:utf-8

from faker import Factory
import urllib2
import urllib
from lxml import etree
import cookielib

f = Factory.create()

class SpiderCisco(object):
    login_url = "https://sso.cisco.com/autho/forms/CDClogin.html#"
    contract_manager_url = 'https://apps.cisco.com/CustAdv/ServiceSales/contract/viewContractMgr.do?method=viewContractMgr'

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'keep-alive',
        'Host': 'sso.cisco.com',
        'User-Agent': f.user_agent(),
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
    # response = urllib2.urlopen(login_url)
    # print response.read()
    c = cookielib.LWPCookieJar()
    # python获取cookies
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(c))

    # 提交参数
    data = urllib.urlencode(formdata)

    # 请求登录
    request = urllib2.Request(login_url,data,headers)
    # request = urllib2.Request(contract_manager_url,data)
    # response = urllib2.urlopen(request)
    # 保存cookies
    response = opener.open(request)
    text = response.read()
    print text

    # 转化成html
    # html = etree.HTML(text)
    # result = etree.tostring(html)
    # print(result)

    # html = etree.parse(text)
    #print type(html)
    #result = html.xpath('//title[1]/text()')
    # print result
    #print len(result)
    # print type(result)
    # print type(result[0])