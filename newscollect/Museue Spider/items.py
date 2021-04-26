Python 3.6.6 (v3.6.6:4cf1f54eb7, Jun 27 2018, 03:37:03) [MSC v.1900 64 bit (AMD64)] on win32
Type "copyright", "credits" or "license()" for more information.
>>> import scrapy


class MuseumnewsItem(scrapy.Item):
    # 博物馆名称 = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    time = scrapy.Field()
    content = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
    tag = scrapy.Field()
    pass
