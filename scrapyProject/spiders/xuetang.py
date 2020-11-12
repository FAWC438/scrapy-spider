import json

import scrapy

from scrapyProject.items import ScrapyprojectItem


class XuetangSpider(scrapy.Spider):
    name = 'xuetang'
    allowed_domains = ['xuetangx.com']
    base_url = 'https://www.xuetangx.com/api/v1/lms/get_product_list/?page='
    page_index = 1
    headers = {
        'accept': 'application/json,text/plain,*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh',
        'content-type': 'application/json',
        'cookie': 'provider=xuetang; django_language=zh',
        'django-language': 'zh',
        'origin': 'https://www.xuetangx.com',
        'referer': 'https://www.xuetangx.com/search?query=&org=&classify=1&type=&status=&page=1',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36 Edg/86.0.622.63',
        'x-client': 'web',
        'xtbz': 'xt'
    }
    payload = {'query': "", 'chief_org': [], 'classify': ["1"], 'selling_type': [], 'status': [], 'appid': 10000}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.download_delay = 1

    def parse(self, response, **kwargs):
        item = ScrapyprojectItem()

        r_data = json.loads(response.text)
        # print(r_data)
        lesson_list = r_data['data']['product_list']
        # print(lesson_list)

        if not lesson_list:
            return

        for lesson in lesson_list:
            item['class_name'] = lesson['name']
            item['teacher'] = ''
            for single_teacher in lesson['teacher']:
                item['teacher'] += (single_teacher['name'] + ' ')
            item['school_name'] = lesson['org']['name']
            item['student_num'] = lesson['enroll_play_num']

            if item['class_name'] and item['teacher'] and item['school_name'] and item['student_num']:
                yield item

        url = self.base_url + str(self.page_index)
        self.page_index += 1
        yield scrapy.Request(
            url=url,
            method='POST',
            headers=self.headers,
            body=json.dumps(self.payload),
            callback=self.parse
        )

    def start_requests(self):
        url = self.base_url + str(self.page_index)
        self.page_index += 1

        yield scrapy.FormRequest(
            url=url,
            method='POST',
            headers=self.headers,
            body=json.dumps(self.payload),
            callback=self.parse
        )
