import scrapy

from scrapyProject.items import ScrapyprojectItem


class LianjiaSpider(scrapy.Spider):
    name = 'lianjia'
    allowed_domains = ['bj.lianjia.com']
    base_url = 'https://bj.lianjia.com/ershoufang/'
    zones = ['dongcheng/', 'xicheng/', 'chaoyang/', 'haidian/']
    zones_chinese = ['东城', '西城', '朝阳', '海淀']
    page_index = 1
    zone_index = 1
    start_urls = [base_url + zones[0]]

    def parse(self, response, **kwargs):
        item = ScrapyprojectItem()

        info_list = response.xpath('//div[@class="info clear"]')
        for info in info_list:
            item['zone_name'] = self.zones_chinese[self.zone_index - 1]
            item['building_names'] = info.xpath('./div[@class="title"]/a/text()').extract()[0]
            item['total_price'] = ''.join(info.xpath(
                './div[@class="priceInfo"]/div[@class="totalPrice"]/span/text()').extract() + info.xpath(
                './div[@class="priceInfo"]/div[@class="totalPrice"]/text()').extract())
            item['area'] = info.xpath(
                './div[@class="address"]/div[@class="houseInfo"]/text()').re('[0-9]+\.[0-9]+平米|[0-9]+平米')[0]
            item['price_per_area'] = info.xpath(
                './div[@class="priceInfo"]/div[@class="unitPrice"]/span/text()').extract()[0]

            if item['building_names'] and item['total_price'] and item['area'] and item['price_per_area']:
                yield item

        self.page_index += 1
        if self.zone_index < len(self.zones):
            if self.page_index <= 5:
                # print(self.page_index)
                # print(self.zone_index)
                url = self.base_url + self.zones[self.zone_index] + 'pg' + str(self.page_index)
            else:
                # print(self.page_index)
                # print(self.zone_index)
                # print(len(self.zones))
                self.page_index = 1
                url = self.base_url + self.zones[self.zone_index]
                self.zone_index += 1
        else:
            return
        yield scrapy.Request(url, callback=self.parse)
        # self.zone_index += 1
        # if self.zone_index < len(self.zones):
        #     url = self.base_url + self.zones[self.zone_index]
        #     scrapy.Request(url, callback=self.parse)
