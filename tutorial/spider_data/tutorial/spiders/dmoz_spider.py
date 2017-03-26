# coding:utf-8
import scrapy
from scrapy.http import FormRequest
from faker import Factory
from tutorial.items import DmozItem
import urlparse


f = Factory.create()


class DmozSpider(scrapy.Spider):
    name = "cisco"
    allowed_domains = ["cisco.com"]

    start_urls = [
       # "https://www.douban.com/",
    ]

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'keep-alive',
        'Host': 'sso.cisco.com',
        'User-Agent': f.user_agent(),
    }

    formdata = {
        'form_email': 'wangyang',
        'form_password': 'p@ssW0RD88',
        # 'target':'',
        # 'smauthreason':'',
        # 'smquerydata':'',
        # 'smagentname':'',
        # 'postpreservationdata':'',
        # 'SMENC':'',
        # 'SMLOCALE':'',
        'source': 'index_nav',
    }

    def start_requests(self):
        print "start_requests"
        print 80 * '$'
        return [scrapy.FormRequest(url='https://sso.cisco.com/autho/forms/CDClogin.html',
                                formdata = self.formdata,
                               headers = self.headers,
                               meta={'cookiejar': 1},
                               callback=self.parse_login)]

    def parse_login(self, response):
        # yield scrapy.Request(link, callback=self.parse_next)
        # for item in response.xpath('/body[1]/table[2]/lbody[1]/tr[1]/td[1]/table[1]/lbody[1]/noscript[1]/div[1]/div[1]/div[1]/form[1]/div[1]/dic[1]/form[2]/div[1]/div[2]/div[2]/table[1]/lbody[1]/tr/'):
        #     print item.xpath('td[2]/a/@title').extract()[0]
        print response.xpath('//title').extract()[0]
        print response.xpath('//title[1]//text()').extract()[0]
        # for item in response.xpath('/body[1]/table[2]/lbody[1]/tr[1]/td[1]/table[1]/lbody[1]/noscript[1]/div[1]/div[1]/div[1]/form[1]/div[1]/dic[1]/form[2]/div[1]/div[2]/div[2]/table[1]/lbody[1]/tr/'):
        #     print item.xpath('td[2]/a/@title').extract()[0]
        # print response.xpath('//body[1]/table[2]/lbody[1]/tr[1]/td[1]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr[1]/td[1]/span[1]').extract()[0]
        print 80*' ok!'
        return [scrapy.FormRequest.from_response(response,
                                   formdata=self.formdata,
                                   callback=self.after_login)]

    def after_login(self, response):
        print "after_login"
        print response.xpath('//title').extract()[0]
        print response.xpath('//title[1]//text()').extract()[0]
        # 查询网址的Cookie
        # 请求Cookie
        Cookie = response.request.headers.getlist('Cookie')
        print 'Cookie', Cookie
        # 响应Cookie
        Cookie = response.headers.getlist('Set-Cookie')
        print 'Set-Cookie', Cookie
        print 80 * '$'
        return [scrapy.FormRequest(url='https://apps.cisco.com/CustAdv/ServiceSales/contract/viewContractMgr.do?method=viewContractMgr#',
#                                   meta={'cookiejar': response.meta['cookiejar']},
                                   callback=self.last_login)]

    def last_login(self, response):
        print "last_login"
        print response.xpath('//title').extract()[0]
        print response.xpath('//title[1]//text()').extract()[0]