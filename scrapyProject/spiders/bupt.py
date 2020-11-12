import scrapy

from scrapyProject.items import ScrapyprojectItem


class BuptSpider(scrapy.Spider):
    name = 'bupt'
    allowed_domains = ['bupt.edu.cn/']
    start_urls = ['https://www.bupt.edu.cn/yxjg1.htm']

    def parse(self, response, **kwargs):
        item = ScrapyprojectItem()
        print('*' * 30)
        # print(response.text)
        print('*' * 30)
        # /html/body/div[2]/div[2]/div[2]/div/ul/li[4]/div/ul/li[1]/a
        # /html/body/div[2]/div[2]/div[2]/div/ul/li[4]/div/ul/li[1]/a
        # /html/body/div[2]/div[2]/div[2]/div/ul/li[4]/div/ul/li[3]/a
        # /html/body/div[2]/div[2]/div[2]/div/ul/li[4]/div/ul/li[14]/a

        for each in response.xpath('//h2[@id="1268"]/following-sibling::div/ul/li/a'):
            print(each.extract())
            print('*' * 30)
            item['school'] = each.xpath('text()').extract()
            item['link'] = each.xpath('@href').extract()
            if item['school'] and item['link']:
                yield item
