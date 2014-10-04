import types
from scrapy.spider import Spider


from scrapy.selector import Selector

from picdown.items import PicdownItem

import scrapy
import picdown.config as config


cur_dict = config.src_dict[config.MY_PIC_SITE]


class PicdownSpider(Spider):
    name = "picdown"
    allowed_domains = ["lofter.com"]
    start_urls = [
        cur_dict['url']
    ]
    DELETE_CHARS = '\n\t\\/:*?\"<>| '
    NAME_TRANS_TABLE = dict([(ord(ch), u'') for ch in u'\n\t\\/:*?\"<>| '])

    def parse(self, response):
        response_sel = Selector(response)
        item = PicdownItem()

        if response.url[-4:] == '.com':
            suburl = response_sel.xpath(cur_dict['maingate_xpath']).extract()
            if suburl:
                self.log('main_jump url: %s' % suburl[0])
                yield scrapy.http.Request(suburl[0], callback=self.parse)
            else:
                yield item
        else:
            for url in response_sel.xpath(cur_dict['next_xpath']).extract():
                self.log('next url: %s' % url)
                yield scrapy.http.Request(url, callback=self.parse)

            item['site_url'] = response.url
            item['time'] = response_sel.xpath(cur_dict['time_xpath']).extract()[:1]
            text = ''.join(response_sel.xpath(cur_dict['text_xpath']).extract())
            self.log('text: %s, type: %s'%(text, type(text)))
            if type(text) == types.UnicodeType:
                item['text'] = [text.translate(self.NAME_TRANS_TABLE)]
            else:
                item['text'] = [text.translate(None, self.DELETE_CHARS)]
            image_urls = []
            links = response_sel.xpath(cur_dict['pic_xpath']).extract()
            for pic in links:
                image_urls.append(pic)
            item['image_urls'] = image_urls
            yield item


