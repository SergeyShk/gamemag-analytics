from datetime import datetime
from scrapy import Request, Spider
from gamemag.items import GamemagItem
from urllib.parse import urljoin

class HelpMyCash(Spider):
    name = "gamemag"
    allowed_domains = ["gamemag.ru"]
    start_urls = ['https://gamemag.ru/reviews']

    def parse(self, response):
        total_pages = int(response.xpath('//li[contains(@class, "page-navigation__link--last")]/a/@href').extract_first().split('/')[-1])
        for page in range(1, total_pages + 1):
            page_url = "/".join([response.url, 'page', str(page)])
            yield Request(url=page_url, callback=self.parse_page)   

    def parse_page(self, response):
        for review in response.xpath('//div[@class="game-listing__game"]/a/@href').extract():
            review_url = urljoin(response.url, review)
            yield Request(url=review_url, callback=self.parse_review)

    def parse_review(self, response):
        item = GamemagItem()
        overview = response.xpath('//div[@class="overview"]')
        item['valuation'] = int(overview.xpath('span/text()').extract_first() or 0)
        item['title'] = overview.xpath('div[3]/h1/text()').extract_first()[6:]
        item['description'] = overview.xpath('div[3]/p/text()').extract_first()
        item['authors'] = '\n'.join([item.strip() for item in overview.xpath('div[3]/div/div[1]/span[2]/a/text()').extract()])
        item['editors'] = '\n'.join([item.strip() for item in overview.xpath('div[3]/div/div[2]/span[2]/a/text()').extract()])
        item['date'] = datetime.strptime(overview.xpath('div[3]/div/div[3]/span[2]/text()').extract_first(), '%d.%m.%Y %H:%M')
        item['comments'] = int(overview.xpath('a[2]/span/text()').extract_first() or 0)
        
        item['visual_overview'] = '\n'.join(response.xpath('//div[@class="visual-overview"]/div[2]/div/span/text()').extract())

        about = response.xpath('//div[@class="about-game"]/div')
        item['platforms'] = '\n'.join([item.strip() for item in about.xpath('div[1]/div/a/text()').extract()])
        item['developers'] = '\n'.join([item.strip() for item in about.xpath('div[2]/div/a/text()').extract()])
        item['publishers'] = '\n'.join([item.strip() for item in about.xpath('div[3]/div/a/text()').extract()])
        item['genres'] = '\n'.join([item.strip() for item in about.xpath('div[4]/p/a/text()').extract()])
        
        item['text'] = '\n'.join(response.xpath('//div[contains(@class, "content-text")]/p/text()').extract())
        item['screenshots'] = len(response.xpath('//div[@id="gallery"]/img').extract())
        
        evaluation = response.xpath('//section[@class="evaluation-of-game"]/div')
        item['passed_on'] = evaluation.xpath('div[1]/div[1]/div/a/text()').extract_first()
        item['theme'] = evaluation.xpath('div[1]/div[2]/span[2]/text()').extract_first()
        item['duration'] = evaluation.xpath('div[1]/div[3]/span[2]/text()').extract_first()
        item['score'] = int(evaluation.xpath('div[2]/div[contains(@class, "active")]/div/span[1]/text()').extract_first())

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
