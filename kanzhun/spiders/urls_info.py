import logging
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
from kanzhun.item import InterviewItem
import re
import json


class UrlsSpider(CrawlSpider):
    name = 'urls'
    host = 'https://www.kanzhun.com'
    start_urls = ['/interviewl/search/?q=&pagenum=6&ka=paging6']
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.basicConfig(
        level=logging.DEBUG,
        format='''%(asctime)s%(filename)s
        [line:%(lineno)d] %(levelname)s %(message)s''',
        datefmt='%a, %d %b %Y %H:%M:%S',
        filename='cataline.log',
        filemode='w')

    # test = True
    def start_requests(self):
        for interview_type in self.start_urls:
            # yield return a generator which can only be used once
            yield Request(
                url='https://www.kanzhun.com/%s' % interview_type,
                callback=self.parse_interview_key)

    def parse_interview_key(self, response):
        selector = Selector(response)
        logging.debug('request url:------>' + response.url)
        # logging.info(selector)
        divs = selector.xpath('//div[@class="wrap_style mt15"]')
        for div in divs:
            # logging.debug('divs :------>' + div.extract())
            viewkey = re.findall('title="(.*?)">', div.extract())
            logging.debug(viewkey)
            # yield Request(
            #     url='https://www.pornhub.com/embed/%s' % viewkey[0],
            #     callback=self.parse_interview_info)
        url_next = selector.xpath(
            '//a[@ka="com1-seeall" and text()="查看更多"]/@href').extract()
        logging.debug(url_next)
        if url_next:
            # if self.test:
            logging.debug(' next page:---------->' + self.host + url_next[0])
            # yield Request(
            #     url=self.host + url_next[0], callback=self.parse_interview_key)
            # self.test = False

    def parse_interview_info(self, response):
        interviewItem = InterviewItem()
        selector = Selector(response)
        logging.info(selector)
        _interview_info = re.findall('(.*?),\n', selector.extract())
        logging.debug('信息的JSON:')
        logging.debug(_interview_info)
        _ph_info_json = json.loads(_interview_info[0])

        duration = _ph_info_json.get('video_duration')
        logging.info('duration:' + duration)
        yield interviewItem
