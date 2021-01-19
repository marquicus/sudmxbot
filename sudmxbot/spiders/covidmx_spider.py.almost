import scrapy
from sudmxbot.models import Daily
import re


class RedditCovidmxSpider(scrapy.Spider):
    name = "covidmx"

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
        (casos, defunciones, fecha) = re.match('(?P<cases>[\w\,\s]+)\s\|\s(?P<deaths>[\w\,\s]+)\s\-\s([\/\d]+)', today_cases).groups()  # noqa W605, E501
        if today_cases:
            self.log(f"Going to create: {today_cases}")
            if Daily.select().where(Daily.fecha == fecha).exists():
                Daily.update({Daily.casos: casos, Daily.defunciones: defunciones}).where(Daily.fecha == fecha).execute()  # noqa E501
            else:
                Daily.create(fecha=fecha, casos=casos, defunciones=defunciones)
        self.log(f'Finished...')
