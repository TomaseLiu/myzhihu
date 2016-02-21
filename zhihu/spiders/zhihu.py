#! /usr/bin/evn python
#encoding=utf-8
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request, FormRequest, HtmlResponse
#from zhihu.items import ZhihuItem

class ZhihuSpider(CrawlSpider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = [
        "http://www.zhihu.com"
    ]
    rules = (
        Rule(SgmlLinkExtractor(allow = ('/question/\d+#.*?', )), callback = 'parse_page', follow = True),
        Rule(SgmlLinkExtractor(allow = ('/question/\d+', )), callback = 'parse_page', follow = True),
    )
    #rules = (
    #    Rule(SgmlLinkExtractor(allow=('/people/tomase-liu', )), callback = 'parse_page', follow = True),
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
        print "Preparing login"
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

    def parse_page(self, response):
        #print "test point"
        response = HtmlResponse(url=response.url, status=response.status, headers=response.headers, body=response.body)
        url = response.url
        name = response.xpath('//h2[@class="zm-item-title zm-editable-content"]/text()').extract()
        context_list = response.xpath('//div[@class="zm-editable-content"]/text()').extract()
        print name[0]
        for context in context_list:
            print context

        answer_num = response.xpath('//h3/@data-num').extract()
        if len(answer_num) == 0:
            print 1
        else:
            print answer_num[0]

        author_list = response.xpath('//*[@class="author-link"]/text()').extract()
        for author in author_list:
            print author
        #print author_list
        #answer_list = response.xpath('//*[@id="zh-question-answer-wrap"]/div[1]/div[1]/button[1]/span[2]/text()').extract()

'''
header2={
    method:next,
    params:{"url_token":37758083,"pagesize":50,"offset":50},
    _xsrf:ce34529bc86c8451d77f11382b55f592
}'''
