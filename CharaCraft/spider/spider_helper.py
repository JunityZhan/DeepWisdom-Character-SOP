import os
import re
import sys

from scrapy.crawler import CrawlerProcess
from spider.spiders.wiki_spider import TextSpider


def safe_filename(filename):
    """Return a safe version of the filename by replacing non-alphanumeric characters."""
    return re.sub(r'[^a-zA-Z0-9_\-]', '_', filename)


def main(start_url, max_depth):
    output_file = safe_filename(os.path.basename(start_url).split("/")[-1]) + ".jsonl"

    settings = {
        'DEPTH_LIMIT': str(max_depth),
        'FEEDS': {
            output_file: {
                'format': 'jsonlines',
                'encoding': 'utf8',
                'store_empty': False,
                'fields': None,
                'indent': 0,
            }
        },
        'ITEM_PIPELINES': {
            "spider.pipelines.GeneralPipeline": 100,
            "spider.pipelines.ConfiguredPipeline": 300,
        }
    }

    process = CrawlerProcess(settings)
    process.crawl(TextSpider, url=start_url)
    process.start()


if __name__ == "__main__":
    start_url_arg = sys.argv[1]
    max_depth_arg = sys.argv[2]
    main(start_url_arg, max_depth_arg)
