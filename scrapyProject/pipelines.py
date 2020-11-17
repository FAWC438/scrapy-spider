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
    csv_writer = csv.DictWriter(csv_file, fieldnames=['class_name', 'teacher', 'school_name', 'student_num'])
    csv_writer.writeheader()

    def process_item(self, item, spider):
        dict_item = dict(item)
        if spider.name == 'xuetang':
            self.csv_writer.writerow(dict_item)
        else:
            json_str = json.dumps(dict_item, ensure_ascii=False) + ',\n'
            self.json_file.write(json_str)
        return item

    def close_spider(self, spider):
        self.json_file.write(']')
        self.csv_file.close()
        self.json_file.close()
