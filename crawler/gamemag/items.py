import scrapy

class GamemagItem(scrapy.Item):
    valuation = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    authors = scrapy.Field()
    editors = scrapy.Field()
    date = scrapy.Field()
    comments = scrapy.Field()
    visual_overview = scrapy.Field()
    platforms = scrapy.Field()
    developers = scrapy.Field()
    publishers = scrapy.Field()
    genres = scrapy.Field()
    text = scrapy.Field()
    screenshots = scrapy.Field()
    passed_on = scrapy.Field()
    theme = scrapy.Field()
    duration = scrapy.Field()
    score = scrapy.Field()
    laugh = scrapy.Field()
    joy = scrapy.Field()
    disgust = scrapy.Field()
    surprise = scrapy.Field()
    anger = scrapy.Field()
    bitterness = scrapy.Field()
    interest = scrapy.Field()
    poker = scrapy.Field()