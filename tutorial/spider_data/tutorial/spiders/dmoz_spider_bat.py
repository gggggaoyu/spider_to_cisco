# coding:utf-8
import scrapy
from scrapy.http import FormRequest
from faker import Factory
from tutorial.items import DmozItem
import urlparse

f = Factory.create()


class DmozSpider(scrapy.Spider):
    name = "cisco_bat"
    allowed_domains = ["sso.cisco.com"]
    # allowed_domains = ["resource-zone.com"]

    start_urls = [
        "https://sso.cisco.com/ autho/forms/CDClogin.html#"
    ]

    def parse(self, response):
        # 请求第一页
        yield scrapy.Request(response.url, callback=self.parse_next)

        # 请求其它页
        # for page in response.xpath('//div[@class="paginator"]/a'):  # 这个位置找到了其他链接
        #     link = page.xpath('@href').extract()[0]
        #     print link
        #     yield scrapy.Request(link, callback=self.parse_next)

    def parse_next(self, response):
        print 10*" ok!"
        # for item in response.xpath('//tr[@class="item"]'):
        #     book = DoubanBookItem()
        #     book['name'] = item.xpath('td[2]/div[1]/a/@title').extract()[0]
        #     book['price'] = item.xpath('td[2]/p/text()').extract()[0]
        #     book['ratings'] = item.xpath('td[2]/div[2]/span[2]/text()').extract()[0]
        #     yield book

    # def start_requests(self):
    #     return [
    #         FormRequest(
    #             "http://web:9312/dynamic/login",
    #             formdata={"user": "user", "pass": "pass"}
    #         )]
    # def parse(self, response):
    #     # filename = response.url.split("/")[-2]
    #     # print 20*'#'
    #     # local_filename = 'D:/odoo/tutorial/spider_data/'+filename
    #     # with open(local_filename, 'wb') as f:
    #     #     f.write(response.body)
    #     for sel in response.xpath('//ul/li'):
    #         title = sel.xpath('a/text()').extract()
    #         link = sel.xpath('a/@href').extract()
    #         desc = sel.xpath('text()').extract()
    #         print title, link, desc

    # headers = {
    #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    #     'Accept-Encoding': 'gzip, deflate, br',
    #     'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    #     'Connection': 'keep-alive',
    #     'Host': 'https://sso.cisco.com/autho/forms/CDClogin.html',
    #     'User-Agent': f.user_agent(),
    # }
    #
    # formdata = {
    #     'form_email': 'wangyang',
    #     'form_password': 'p@ssW0RD88',
    #     # 'captcha-solution': '',
    #     # 'captcha-id': '',
    #     'login': '登录',
    #     'redir': 'https://sso.cisco.com/autho/forms/CDClogin.html',
    #     'source': 'None'
    # }
    #
    # def start_requests(self):
    #     return [scrapy.Request(url='https://www.douban.com/accounts/login',
    #                            headers=self.headers,
    #                            meta={'cookiejar': 1},
    #                            callback=self.parse_login)]
    #
    # def parse_login(self, response):
    #     # 如果有验证码要人为处理
    #     if 'captcha_image' in response.body:
    #         print 'Copy the link:'
    #         link = response.xpath('//img[@class="captcha_image"]/@src').extract()[0]
    #         print link
    #         captcha_solution = raw_input('captcha-solution:')
    #         captcha_id = urlparse.parse_qs(urlparse.urlparse(link).query, True)['id']
    #         self.formdata['captcha-solution'] = captcha_solution
    #         self.formdata['captcha-id'] = captcha_id
    #     return [scrapy.FormRequest.from_response(response,
    #                                              formdata=self.formdata,
    #                                              headers=self.headers,
    #                                              meta={'cookiejar': response.meta['cookiejar']},
    #                                              callback=self.after_login
    #                                              )]
    #
    # def after_login(self, response):
    #     print response.status
    #     self.headers['Host'] = "www.douban.com"
    #     return scrapy.Request(url='https://www.douban.com/doumail/',
    #                           meta={'cookiejar': response.meta['cookiejar']},
    #                           headers=self.headers,
    #                           callback=self.parse_mail)
    #
    # def parse_mail(self, response):
    #     print response.status
    #     for item in response.xpath('//div[@class="doumail-list"]/ul/li'):
    #         mail = DoubanMailItem()
    #         mail['sender_time'] = item.xpath('div[2]/div/span[1]/text()').extract()[0]
    #         mail['sender_from'] = item.xpath('div[2]/div/span[2]/text()').extract()[0]
    #         mail['url'] = item.xpath('div[2]/p/a/@href').extract()[0]
    #         mail['title'] = item.xpath('div[2]/p/a/text()').extract()[0]
    #         print mail
    #         yield mail