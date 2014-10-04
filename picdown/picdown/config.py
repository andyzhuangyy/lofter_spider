#/bin/env python
__author__ = 'zhuangyongyao'

# dearpp
# wanimal
MY_PIC_SITE = 'wanimal'



src_dict = {
    'wanimal': {
        'url': 'http://wanimal.lofter.com',
        'pic_xpath': '//a[@class="imgclasstag"]/@bigimgsrc',
        'time_xpath': '//div[@class="info"]/a/text()',
        'text_xpath': '//div[@class="txt"]/p/text()',
        'next_xpath': '//a[@class="nxt"]/@href',
        'maingate_xpath': '//div[@class="info"]/a/@href',
    },
    'dearpp': {
        'url': 'http://dearpp.lofter.com',
        'pic_xpath': '//div[@class="pic"]/a/@bigimgsrc',
        'time_xpath': '//a[@class="date"]/text()',
        'text_xpath': '//div[@class="text"]/p/text()',
        'next_xpath': '//a[@class="next"]/@href',
        'maingate_xpath': '//div[@class="pic"]/a[@class="img"]/@href',
    },
}
