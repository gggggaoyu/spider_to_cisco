# coding:utf-8
import re

import requests
import scrapy
from faker import Factory

# from tutorial.items import DmozItem,PageItem,SumbitItem

f = Factory.create()


class DmozSpider(scrapy.Spider):
    name = "cisco"
    allowed_domains = ["cisco.com"]

    start_urls = [
        'https://sso.cisco.com/autho/login/loginaction.html',
    ]

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
        # 'Referer': 'https://apps.cisco.com/CustAdv/ServiceSales/contract/viewContractMgr.do?method=viewContractMgr',
    }
    contract_urls = []
    contract_go_urls = []
    download_select_urls = []

    def start_requests(self):
        return [scrapy.FormRequest(url='https://sso.cisco.com/autho/login/loginaction.html',
                                   # url='https://apps.cisco.com/CustAdv/ServiceSales/contract/viewContractMgr.do?method=viewContractMgr',
                                   formdata=self.formdata,
                                   headers=self.headers,
                                   meta={'cookiejar': 1},
                                   callback=self.after_login)]

    def after_login(self, response):
        print "after_login"
        return [scrapy.FormRequest(
            url='https://apps.cisco.com/CustAdv/ServiceSales/contract/viewContractMgr.do?method=viewContractMgr',
            meta={'cookiejar': response.meta['cookiejar']},
            callback=self.parse_contract_manager)]

    # 进入合同管理页面
    count = 0
    def parse_contract_manager(self, response):
        self.tableID = response.xpath('//*[@id = "tableIdForActions"]/@value').extract()[0]
        self.contextID = response.xpath('//*[@id = "cmContextForActions"]/@value').extract()[0]
        self.pages = response.xpath('//*[@id = "mod_2"]/table/tbody/tr/td[2]/text').extract()
        # self.count = self.count + 1
        print self.tableID
        print self.contextID
        rlist=[]
        for page in range(1):
            url2 = r'https://apps.cisco.com/CustAdv/ServiceSales/contract/performTableActions.do?sortID=contractNumber&pageID=' + str(
                page + 1) + '&tableID=' + self.tableID + '&contextID=' + self.contextID + '&method=paginateContracts&cmToLine=undefined&selectedProductsCHR=&currentPageId=1'
            print url2
            #yield scrapy.FormRequest(url=url2, meta={'cookiejar': response.meta['cookiejar']},callback=self.collect_urls)
            # print url2

            # rlist.append(scrapy.FormRequest(url=url2, meta={'cookiejar': response.meta['cookiejar']},
            # callback = self.collect_urls))
            yield scrapy.FormRequest(url=url2, meta={'cookiejar': response.meta['cookiejar']},
                               callback=self.collect_urls)
        print "page执行完了2"
        # print self.contract_urls
        # return rlist

    def collect_urls(self, response):
        print response
        print "collect"
        items = response.xpath('//*[@id="cmDataDiv"]/table/tbody/tr')
        print items
        print len(items)
        rlist=[]
        for item in items:
            if item.xpath('td[2]/a/@href').extract():
                value_test = item.xpath('td[2]/a/@href').extract()[0]
                print value_test
                value = item.xpath('td[2]/a/@href').extract()[0][1:]
                # print "访问合同管理中心"
                url = 'https://apps.cisco.com/CustAdv/ServiceSales/contract' + value
                #print url
                #self.contract_urls.append(url)
                rlist.append(scrapy.FormRequest(url=url, meta={'cookiejar': response.meta['cookiejar']},
                                         callback=self.contract_center))
            print "kanzhege"
        # print self.contract_urls
        # print len(self.contract_urls)
        # print rlist
        print len(rlist)
        return rlist

        # yield scrapy.FormRequest(url=url, meta={'cookiejar': response.meta['cookiejar']},
        #                          callback=self.contract_center)

    # 选取下载合同的选项，点击GO
    count = 1
    def contract_center(self, response):
        title_href = response.xpath('//title[1]').extract()[0]
        print "模拟点击GO"
        script_text = response.xpath('//*[@id="mod_1"]/script/text()').extract()[0]
        # if re.compile('case\s\'Download Contract or Selected Data\':[\s|\S]*?url = checkBrowser\(\'(.*?)\'\);').findall(
        #     script_text):
        url_half = re.compile('case\s\'Download Contract or Selected Data\':[\s|\S]*?url = checkBrowser\(\'(.*?)\'\);').findall(
            script_text)[0]
        print url_half
        print type(url_half)
        url3 = 'https://apps.cisco.com/CustAdv/ServiceSales/contract/' + url_half
        print url3
        # 进入待下载页面
        # self.contract_go_urls.append(url3)
        # return  self.contract_go_urls
        self.count = self.count + 1
        print self.count
        return scrapy.FormRequest(url=url3,
                                 meta={'cookiejar': response.meta['cookiejar']},
                                 callback=self.download_select
                                 )


    # 点击product+con 点击save now 点击sumbit
    flag = 0
    def download_select(self, response):

        self.flag = self.flag + 1
        print self.flag, 'test'

        with open(r'e:' +'response'+str(self.flag)+ '.html', 'wb') as code:
            code.write(response.body)
        dic = {}
        seqId = response.xpath('//*[@id="seqId"]/@value').extract()[0]        # dic['ServiceLineId'] = response.xpath('//*[@id="ServiceLineId"]/@value').extract()[0]
        ServiceLineId = response.xpath('//*[@id="ServiceLineId"]/@value').extract()[0]
        ContractNumber = response.xpath('//*[@id="ContractNumber"]/@value').extract()[0]
        #// *[ @ id = "ContractNumber"]
        # print self.ContractNumber
        print "0000000000---%s" % (response.url)
        print "0000000000---%s"%(ContractNumber)
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
        print "设置完参数等待下载",str(ContractNumber),str(ServiceLineId),str(seqId)
        title_href = response.xpath('//title[1]').extract()[0]
        title = response.xpath('//title[1]/text()').extract()[0]
        # self.download_select_urls.append(dic)
        # return SumbitItem
        # 提交新的formdata,请求真正的URL，action是下载
        return [scrapy.FormRequest(url='https://apps.cisco.com/CustAdv/ServiceSales/contract/downloadContractSelectedData.do?methodName=onSubmitDataForm',
                                   # url='https://apps.cisco.com/CustAdv/ServiceSales/contract/viewContractMgr.do?method=viewContractMgr',
                                   formdata=formdata_b,
                                   meta={'cookiejar': response.meta['cookiejar']},
                                   callback=self.bb_download_contract(ContractNumber)
                                   )]

    # def bb_download_contract(self, response):
    #     pass
    flags = 0
    def bb_download_contract(self, ContractNumber):
        def download_contract(response):
            self.flags = self.flags + 1
            # title_href = response.xpath('//title[1]').extract()[0]
            # title = response.xpath('//title[1]/text()').extract()[0]
            print (response.url)
            print dir(response.request)
            # print "这个是返回了什么呢？"
            r = requests.get(response.url, headers=response.request.headers)
            print dir(r)
            print "=====ContractNumber:%s"%ContractNumber
            # print self.flags
            # with open(r'e:' + str(self.flags) + '.zip', 'wb') as code:
            #     code.write(r.content)
                # print r.raw
            print self.flags
        return download_contract