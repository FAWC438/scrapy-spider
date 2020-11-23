import scrapy

from scrapyProject.items import ScrapyprojectItem


class LoupanSpider(scrapy.Spider):
    name = 'loupan'
    allowed_domains = ['bj.fang.lianjia.com']
    base_url = 'https://bj.fang.lianjia.com/loupan/pg'
    page_index = 1
    start_urls = [base_url + str(page_index)]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.download_delay = 5

    def parse(self, response, **kwargs):
        item = ScrapyprojectItem()

        info_list = response.xpath('//div[@class="resblock-desc-wrapper"]')

        if not info_list or self.page_index > 19:
            return

        for info in info_list:

            item['name'] = info.xpath('./div[@class="resblock-name"]/a/text()').get()
            if item['name'] is not None:
                item['name'] = item['name'].strip()

            item['location_district'] = info.xpath('./div[@class="resblock-location"]/span[1]/text()').get()
            if item['location_district'] is not None:
                item['location_district'] = item['location_district'].strip()

            item['location_place'] = info.xpath('./div[@class="resblock-location"]/span[2]/text()').get()
            if item['location_place'] is not None:
                item['location_place'] = item['location_place'].strip()

            item['location_detail'] = info.xpath('./div[@class="resblock-location"]/a/text()').get()
            if item['location_detail'] is not None:
                item['location_detail'] = item['location_detail'].strip()

            item['room_type'] = info.xpath('./a[@class="resblock-room"]/span[1]/text()').get()
            if item['room_type'] is not None:
                item['room_type'] = item['room_type'].strip()

            ra = info.xpath('./div[@class="resblock-area"]/span/text()')
            if ra.get() is None:
                item['room_area'] = None
            else:
                item['room_area'] = int(ra.re('\d+')[0])

            tp = info.xpath('./div[@class="resblock-price"]/div[@class="second"]/text()')
            if tp.get() is None:
                item['total_price'] = None
            else:
                item['total_price'] = format(float(tp.re('\d+')[0]), '.4f') + '\t'

            ap = info.xpath(
                './div[@class="resblock-price"]/div[@class="main-price"]/span[1]/text()')
            if ap.get() is None:
                item['average_price'] = None
            elif '总价' in info.xpath('./div[@class="resblock-price"]/div[@class="main-price"]/span[2]/text()').get():
                item['average_price'] = None
                item['total_price'] = format(float(ap.re('\d+')[0]), '.4f') + '\t'
            else:
                item['average_price'] = int(ap.re('\d+')[0])

            if item['name']:
                if item['total_price'] and item['average_price']:
                    yield item
                elif item['room_area'] and item['total_price'] is None and item['average_price']:
                    item['total_price'] = format(float(item['room_area'] * item['average_price'] / 10000), '.4f') + '\t'
                    yield item
                elif item['room_area'] and item['total_price'] and item['average_price'] is None:
                    item['average_price'] = int(float(item['total_price'][:-1]) * 10000 / item['room_area'])
                    yield item

        self.page_index += 1
        url = self.base_url + str(self.page_index)
        yield scrapy.Request(url, callback=self.parse)
