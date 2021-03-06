import scrapy
from sudmxbot.items import DailyItem
import re


class RedditCovidmxSpider(scrapy.Spider):
    name = "covidmx"
    feedre = re.compile('(?P<cases>[\w\,\s]+)\s\|\s(?P<deaths>[\w\,\s]+)\s\-\s([\/\d]+)')  # noqa W605

    def start_requests(self):
        urls = [
            'https://www.reddit.com/r/covidmx/?f=flair_name%3A%22Im%C3%A1genes%22',
            # 'https://www.reddit.com/r/covidmx/?f=flair_name%3A%22Noticias%22',
        ]
        for url in urls:
            print(url)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        today_cases = response.xpath("//h3[contains(text(), 'Casos Confirmados') \
            and @class='_eYtD2XCVieq6emjKBH3m']/text()").get()
        if today_cases:
            item = DailyItem()
            (item["casos"], item["defunciones"], item["fecha"]) = self.feedre.match(today_cases).groups()
            self.log(f"Going to create: {today_cases}")
            yield item
        self.log(f'Finished...')
