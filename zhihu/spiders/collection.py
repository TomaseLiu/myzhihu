#! /usr/bin/evn python
#encoding=utf-8
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request, FormRequest, HtmlResponse
#from zhihu.items import ZhihuItem

class ZhihuSpider(CrawlSpider):
    name = 'collection'
    allowed_domains = ['www.zhihu.com']
    start_urls = [
        "http://www.zhihu.com/collection/42487937"
    ]
    #rules = (
    #    Rule(SgmlLinkExtractor(allow = ('/question/\d+#.*?', )), callback = 'parse_page', follow = True),
    #    Rule(SgmlLinkExtractor(allow = ('/question/\d+', )), callback = 'parse_page', follow = True),
    #)
    #rules = (
    #    Rule(SgmlLinkExtractor(allow=('/people/tomase-liu', )), callback = 'parse_page', follow = False),
    #)

    headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip,deflate",
    "Accept-Language": "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4",
    "Connection": "keep-alive",
    "Content-Type":" application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
    "Referer": "http://www.zhihu.com/"
    }

    def start_request(self):
        return [Request("https://www.zhihu.com/login/email", meta = {'cookiejar' : 1}, callback = self.post_login)]
    
    def post_login(self, response):
        #print "Preparing login"
        xsrf = Selector(response).xpath('//input[@name="_xsrf"]/@value').extract()[0]
        print xsrf
        return [FormRequest.from_response(response, 
                                            meta = { 'cookiejar': response.meta['cookiejar']},
                                            headers = self.headers,
                                            formdata = {
                                            '_xsrf': xsrf,
                                            'email': '297913634@qq.com',
                                            'password': ''
                                            },
                                            callback = self.after_login,
                                            dont_filter = True
                                            )]

    def after_login(self, response):
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse(self, response):
        print "test point"
        response = HtmlResponse(url=response.url, status=response.status, headers=response.headers, body=response.body)
        url = response.url
        #first_active = response.xpath('//*[@id="zh-profile-activity-page-list"]/div/div[1]/a').extract()
        
#        active_page_list = response.xpath('//*[@id="zh-list-answer-wrap"]/div/h2/a/text()').extract()
        active_page_list = response.xpath('//*[@id="zh-list-answer-wrap"]/div')
        file_obj = open('collection_now.log', 'w')

        for active_block in active_page_list:
            #active = active_block.xpath('.//div[1]/text()').extract()[1].strip()
            #question = active_block.xpath('.//div[1]/a[@class="question_link" or @class="post-link"]/text()').extract()
            #answer_link = active_block.xpath('.//div[1]/a[@class="question_link" or @class="post-link"]/@href').extract()[0]
            
            #if 'http' not in answer_link:
            #    answer_link = "http://www.zhihu.com" + answer_link
            question = active_block.xpath('.//h2/a/text()').extract()[0]
#            answer_link = active_block.xpath('.//div/div[1]/div[4]/div/a[@href="toggle-expand"]/@href').extract()
            answer_link = active_block.xpath('.//div/div[1]/div[4]/div/a/@href').extract()
            if len(answer_link) > 0:
                if 'http' not in answer_link[0]:
                    answer_link_str = "http://www.zhihu.com" + answer_link[0]
#                print question, answer_link_str
                file_obj.write(question.encode('utf-8') + '\t' + answer_link_str.encode('utf-8') + '\n')

#            file_obj.write('\n')

        file_obj.close()


