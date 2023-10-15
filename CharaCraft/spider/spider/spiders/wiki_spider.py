import re

import scrapy
from urllib.parse import urlparse

from ..items import SpiderItem

class TextSpider(scrapy.Spider):
    name = 'text'

    def __init__(self, url=None, *args, **kwargs):
        super(TextSpider, self).__init__(*args, **kwargs)
        if url is None:
            raise ValueError("A target URL is required. Use the 'url' argument to specify one.")
        self.start_urls = [url]
        self.allowed_domains = [urlparse(url).netloc]  # derive allowed domain from URL

    def parse(self, response):
        # Initialize an empty list to hold the text from each element
        all_text = []
        all_text = response.xpath(
            '(//div)/descendant-or-self::text()[not(ancestor::script) and not(ancestor-or-self::*[contains(@style, '
            '"display: none")])]').extract()


        all_text_str = ''.join(all_text).strip()

        item = SpiderItem()
        item['url'] = response.url
        item['text'] = all_text_str
        yield item
        # Discover and follow links to other pages on the same domain
        for href in response.css('a::attr(href)').extract():
            next_page = response.urljoin(href)
            if self.allowed_domains[0] in next_page:
                yield scrapy.Request(next_page, callback=self.parse)
