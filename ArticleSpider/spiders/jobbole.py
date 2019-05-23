# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from urllib import parse

class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    # start_urls = ['http://blog.jobbole.com/']
    # start_urls = ['http://blog.jobbole.com/110287/']
    start_urls =['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        # 解析列表业中的所有文章url并交给scrapy下载后并进行解析
        post_urls =response.css("#archive a.archive-title::attr(href)")
        for post_url in post_urls:
            yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse_detail)

        # 提取下一页并交给scrapy进行下载
        next_urls =response.css(".next.page-numbers::attr(href)").extract_first("")
        if next_urls:
            yield Request(url=parse.urljoin(response.url, next_urls), callback=self.pase)

    def parse_detail(self,response):
        #提取文章的具体子弹
        title = response.xpath("//div[@class='entry-header']/h1/text()").extract()[0]
        create_date = response.xpath("//p[@class='entry-meta-hide-on-mobile']/text()").extract()[0].strip().replace("·","").strip()
        praise_nums = response.xpath("//span[contains(@class,'vote-post-up')]/h10/text()").extract()[0]
        fav_nums = response.xpath("//span[contains(@class,'bookmark-btn')]/text()").extract()[0]
        match_re = re.match(".*(\d+).*", fav_nums)
        if match_re:
            fav_nums = match_re.group(1)

        comment_nums = response.xpath("//a[@href='#article-comment']/span/text()").extract()[0]
        match_re = re.match(".*(\d+).*", comment_nums)
        if match_re:
            comment_nums = match_re.group(1)

        content = response.xpath("//div[@class='entry-header']").extract()[0]
        tag_list = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()[0]
        tag_list =  [element for element in tag_list if not element.strip().endswith("评论")]
        tags = ",".join(tag_list)
        print(tags)
        pass
