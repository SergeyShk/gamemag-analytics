import re
from datetime import datetime
from scrapy import Request, Spider
from gamemag.items import NewsItem
from urllib.parse import urljoin

class NewsSpider(Spider):
    name = "news"
    allowed_domains = ["gamemag.ru"]
    start_urls = ['https://gamemag.ru/news']

    def parse(self, response):
        total_pages = int(response.xpath('//li[contains(@class, "page-navigation__link--last")]/a/@href').extract_first().split('/')[-1])
        for page in range(1, total_pages + 1):
            page_url = "/".join([response.url, 'page', str(page)])
            yield Request(url=page_url, callback=self.parse_page)   

    def parse_page(self, response):
        for review in response.xpath('//div[@class="news-item__top"]/a/@href').extract():
            review_url = urljoin(response.url, review)
            yield Request(url=review_url, callback=self.parse_news)

    def parse_news(self, response):
        item = NewsItem()
        overview = response.xpath('//div[@class="overview"]')
        item['valuation'] = int(overview.xpath('span/text()').extract_first() or 0)
        item['title'] = overview.xpath('div[3]/h1/text()').extract_first()[6:]
        item['authors'] = '\n'.join([item.strip() for item in overview.xpath('div[3]/div/div[1]/span[2]/a/text()').extract()])
        item['date'] = datetime.strptime(overview.xpath('div[3]/div/div[2]/span[2]/text()').extract_first(), '%d.%m.%Y %H:%M')
        item['comments'] = int(overview.xpath('a/span/text()').extract_first() or 0)

        about = response.xpath('//div[@class="about-game"]/div')
        item['platforms'] = '\n'.join([item.strip() for item in about.xpath('div[1]/div/a/text()').extract()])
        item['categories'] = '\n'.join([item.strip() for item in about.xpath('div[2]/div/a/text()').extract()])
        item['tags'] = '\n'.join([item.strip() for item in about.xpath('div[3]/div/a/text()').extract()])
        item['website'] = about.xpath('div[4]/a/@href').extract_first()
        
        HTML_RE = re.compile(r'<[^>]+>')
        text = HTML_RE.sub('', '\n'.join([item.strip() 
                for item in response.xpath('//div[@class="content-text"]/div/text()|//div[@class="content-text"]/p|strong').extract()[:-2]
                if item.strip() and len(item) > 1]))
        if len(text) < 50:
            text = HTML_RE.sub('', '\n'.join([item.strip() 
                for item in response.xpath('//div[@class="content-text"]').extract()
                if item.strip() and len(item) > 1]))
        item['text'] = text.replace('\xa0', ' ')

        emotions = response.xpath('//div[@class="emotion-rating"]/div[2]')
        item['laugh'] = int(emotions.xpath('//span[contains(@class, "gm-btn__emotion-rating-laugh")]/following-sibling::span/span/text()').extract_first() or 0)
        item['joy'] = int(emotions.xpath('//span[contains(@class, "gm-btn__emotion-rating-joy")]/following-sibling::span/span/text()').extract_first() or 0)
        item['disgust'] = int(emotions.xpath('//span[contains(@class, "gm-btn__emotion-rating-disgust")]/following-sibling::span/span/text()').extract_first() or 0)
        item['surprise'] = int(emotions.xpath('//span[contains(@class, "gm-btn__emotion-rating-surprise")]/following-sibling::span/span/text()').extract_first() or 0)
        item['anger'] = int(emotions.xpath('//span[contains(@class, "gm-btn__emotion-rating-anger")]/following-sibling::span/span/text()').extract_first() or 0)
        item['bitterness'] = int(emotions.xpath('//span[contains(@class, "gm-btn__emotion-rating-bitterness")]/following-sibling::span/span/text()').extract_first() or 0)
        item['interest'] = int(emotions.xpath('//span[contains(@class, "gm-btn__emotion-rating-interest")]/following-sibling::span/span/text()').extract_first() or 0)
        item['poker'] = int(emotions.xpath('//span[contains(@class, "gm-btn__emotion-rating-poker")]/following-sibling::span/span/text()').extract_first() or 0)

        yield item
