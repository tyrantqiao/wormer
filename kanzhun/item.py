from scrapy import Item
import scrapy


class InterviewItem(Item):
    company = scrapy.Field()
    interviewee = scrapy.Field()
