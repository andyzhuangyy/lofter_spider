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
            item['text'] = response_sel.xpath(cur_dict['text_xpath']).extract()

            #filepre = '?filepre=' + item['time'][0] + '-' + '-'.join(item['text'])
            #filepre = '?1234'
            filepre = ''
            image_urls = []
            links = response_sel.xpath(cur_dict['pic_xpath']).extract()
            for pic in links:
                image_urls.append(pic + filepre)
            item['image_urls'] = image_urls
            yield item


