# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import hashlib
import scrapy
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy import log

class PicdownPipeline(object):
    def process_item(self, item, spider):
        print 'process_item'
        return item

class MyimagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        print 'get_media_requests'
        text = ''.join(item['text'])
        time = ''.join(item['time'])
        log.msg('pic text: %s'%text, level=log.DEBUG)
        for i, image_url in enumerate(item['image_urls']):
            log.msg('image: ' + image_url, level=log.DEBUG)
            numstr = str(i + 1)
            yield scrapy.http.Request(image_url,
                meta={'image_text': text,
                      'image_time': time,
                      'image_num' : numstr
                })

    # this is where the image is extracted from the HTTP response
    def get_images(self, response, request, info):
        print "get_images"
        for key, image, buf, in super(MyimagePipeline, self).get_images(response, request, info):
            url = request.url
            hashstr = hashlib.sha1(url).hexdigest()  # change to request.url after deprecation
            key = self.change_filename(key, hashstr, response)
            yield key, image, buf

    def change_filename(self, key, hashstr, response):
        return "full/%s-%s/%s-%s.jpg" % (response.meta['image_time'], response.meta['image_text'], response.meta['image_num'], hashstr)


    def item_completed(self, results, item, info):
        print 'result: ', results
        print 'item: ', item
        print 'info: ', dir(info)
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item

