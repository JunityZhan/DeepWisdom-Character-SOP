import re

import scrapy
from urllib.parse import urlparse


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
        # Splitting into lines, stripping leading/trailing spaces from each line,
        # and filtering out blank lines and lines with 2 words or fewer
        lines = [line.strip() for line in all_text_str.split('\n') if line.strip() and len(line.split()) > 2]
        print(len(lines))
        # Joining lines back into a single string with a single newline character between each line
        lines = [re.sub(r'\s+', ' ', line) for line in lines]
        all_text_str = '\n'.join(lines)

        with open('output.txt', 'a', encoding='utf-8') as f:
            f.write(all_text_str + '\n')

        # Discover and follow links to other pages on the same domain
        for href in response.css('a::attr(href)').extract():
            next_page = response.urljoin(href)
            if self.allowed_domains[0] in next_page:
                yield scrapy.Request(next_page, callback=self.parse)
