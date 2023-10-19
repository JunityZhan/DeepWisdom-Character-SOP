import re
from urllib.parse import urlparse

import scrapy

from ..items import SpiderItem


class TextSpider(scrapy.Spider):
    name = 'text'

    def __init__(self, url=None, *args, **kwargs):
        super(TextSpider, self).__init__(*args, **kwargs)
        if url is None:
            raise ValueError("A target URL is required. Use the 'url' argument to specify one.")
        self.start_urls = [url]
        self.allowed_domains = [urlparse(url).netloc]  # Derive allowed domain from the provided URL

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(TextSpider, cls).from_crawler(crawler, *args, **kwargs)
        # Retrieve the depth limit setting
        spider.limit_depth = crawler.settings.getint('LIMIT_DEPTH', default=0)
        return spider

    def parse(self, response):
        """Extract text from the page and follow links within the allowed domain."""
        # Extract text from the page, excluding content within scripts or hidden elements
        all_text = response.xpath(
            '(//div)/descendant-or-self::text()[not(ancestor::script) and not(ancestor-or-self::*[contains(@style, '
            '"display: none")])]').extract()
        all_text_str = ''.join(all_text).strip()

        # Populate and yield the item
        item = SpiderItem()
        item['url'] = response.url
        item['text'] = all_text_str
        yield item

        # Check the depth of the current page
        current_depth = response.meta.get('depth', 0)
        # Follow links to other pages if the depth is within the limit
        if current_depth < self.limit_depth:
            for href in response.css('a::attr(href)').extract():
                next_page = response.urljoin(href)
                if self.allowed_domains[0] in next_page:
                    yield scrapy.Request(next_page, callback=self.parse)
