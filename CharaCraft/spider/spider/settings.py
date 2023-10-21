# Scrapy settings for spider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'spider'

SPIDER_MODULES = ['spider.spiders']
NEWSPIDER_MODULE = 'spider.spiders'

# from shutil import which
#
# SELENIUM_DRIVER_NAME = 'chrome'
# SELENIUM_DRIVER_EXECUTABLE_PATH = which('geckodriver')
# SELENIUM_DRIVER_ARGUMENTS=['--headless']  # '--headless' if using chrome instead of firefox
# DOWNLOADER_MIDDLEWARES = {
#     'spider.middlewares.RandomHeaderMiddleWare': 545,
# }
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "spider (+http://www.yourdomain.com)"
# DOWNLOAD_DELAY = 2
# CONCURRENT_REQUESTS_PER_DOMAIN = 1
# Obey robots.txt rules
ROBOTSTXT_OBEY = False
HTTPERROR_ALLOWED_CODES  =[404]

ITEM_PIPELINES = {
    'spider.pipelines.GeneralPipeline': 100,
    'spider.pipelines.ConfiguredPipeline': 300,
}
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'
TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'
FEEDS = {
    'output.jsonl': {
        'format': 'jsonlines',  # Using JSON Lines format for simplicity
        'encoding': 'utf8',
        'store_empty': False,
        'fields': None,
        'indent': 0,
    },
}