# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
import json,requests
from ..items import *


class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['careers.tencent.com']
    one_url = 'https://careers.tencent.com/tencentcareer/api/post/Query?timestamp=1566266592644&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword={}&pageIndex={}&pageSize=10&language=zh-cn&area=cn'
    two_url = 'https://careers.tencent.com/tencentcareer/api/post/ByPostId?timestamp=1566266695175&postId={}&language=zh-cn'
    keyword = input("请输入职位类型:")
    headers = {"User-Agent":'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
    keyword = parse.quote(keyword)
    def start_requests(self):
        """把所有一级页面的url地址交给调度器如队列"""
        total = self.total()
        for index in range(1,total+1):
            url = self.one_url.format(self.keyword,index)

            yield scrapy.Request(url=url,callback=self.parse_one_page)

    def total(self):
        url = self.one_url.format(self.keyword,1)
        html = requests.get(url=url,headers=self.headers).json()
        total = html['Data']['Count']
        return total

    def parse_one_page(self, response):
        #获取响应内容 - 字符串
        html = json.loads(response.text)
        for data in html["Data"]["Posts"]:
            item = TencentItem()
            item['post_id'] = data['PostId']
            item['job_url'] = self.two_url.format(item['post_id'])

            yield scrapy.Request(url=item['job_url'],meta={'item':item},callback=self.parse_two_page)

    def parse_two_page(self,response):
        item = response.meta['item']
        html = json.loads(response.text)
        # 名称+类别+职责+要求+地址+时间
        item['job_name'] = html['Data']['RecruitPostName']
        item['job_type'] = html['Data']['CategoryName']
        item['job_duty'] = html['Data']['Responsibility']
        item['job_require'] = html['Data']['Requirement']
        item['job_address'] = html['Data']['LocationName']
        item['job_time'] = html['Data']['LastUpdateTime']

        yield item
