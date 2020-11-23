# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
import csv
import json


class ScrapyprojectPipeline:
    json_file = open('JsonData.json', "w", encoding="utf-8")
    json_file.write('[\n')
    csv_file = open('CsvData.csv', "w", newline='', encoding="utf_8_sig")
    csv_writer_xuetang = csv.DictWriter(csv_file,
                                        fieldnames=['class_name', 'teacher', 'school_name', 'student_num'])
    # csv_writer_xuetang.writeheader()
    csv_writer_loupan = csv.DictWriter(csv_file,
                                       fieldnames=['name', 'location_district', 'location_place', 'location_detail',
                                                   'room_type', 'room_area', 'total_price', 'average_price'])
    csv_writer_loupan.writeheader()

    def process_item(self, item, spider):
        dict_item = dict(item)
        if spider.name == 'xuetang':
            self.csv_writer_xuetang.writerow(dict_item)
        elif spider.name == 'loupan':
            self.csv_writer_loupan.writerow(dict_item)
        else:
            json_str = json.dumps(dict_item, ensure_ascii=False) + ',\n'
            self.json_file.write(json_str)
        return item

    def close_spider(self, spider):
        self.json_file.write(']')
        self.csv_file.close()
        self.json_file.close()
