# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json
import MySQLdb
import MySQLdb.cursors

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi

class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonWithEncodingPipeline(object):
    # 自定义json文件的导出
    def __init__(self):
        self.file = codecs.open("article.json", "w", "utf-8")

    def process_item(self, item, spider):
        lines =json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        self.file.close()

class JsonExporterPipleline(object):
    #调用scrapy提供的json export 导出json文件
    def __init__(self):
        self.file = open("articleexport.json", "wb")
        self.exporter =JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        for ok, value in results:
            image_file_path = value["path"]
        item["front_image_path"] =image_file_path

        return item

class MysqlPipeline(object):
    #采取同步的机制写入数据库
    def __init__(self):
        try:
            self.conn = MySQLdb.connect('127.0.0.1', 'root', '111111', 'article_spider', charset='utf8', use_unicode=True)
        except Exception as e:
            exit(e)

        self.cursor =self.conn.cursor()
    def process_item(self, item, spider):
        insert_sql ="""
            insert into jobbole_article
            (title,create_date,url,url_object_id,praise_nums,comment_nums,fav_nums,tags,front_image_url,content)
            values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        result = self.cursor.execute(insert_sql, (item["title"], item["create_date"], item["url"], item["url_object_id"], item["praise_nums"], item["comment_nums"], item["fav_nums"], item["tags"], item["front_image_url"], item["content"]))
        # print(result)
        self.conn.commit()

        # try:
        #     insert_sql = """
        #                         insert into jobbole_article
        #                         (title,create_date,url,url_object_id)
        #                         values(%s,%s,%s,%s)
        #                     """
        #     self.cursor.execute(insert_sql, (item["title"], item["create_date"], item["url"], item["url_object_id"]))
        #     self.conn.commit()
        # except Exception as e:
        #     exit(e)

class MysqlTwistedPipeline(object):
    def __init__(self, dbpool ):
        self.dbpool=dbpool

    @classmethod
    def from_setting(cls, setting):
        dbparms = dict(
            host=setting["MYSQL_HOST"],
            db=setting["MYSQL_DBNAME"],
            user=setting["MYSQL_USER"],
            passwd=setting["MYSQL_PASSWORD"],
            chartset="utf8",
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpoll=adbapi.ConnectionPool("MySQLdb", **dbparms)
        return cls(dbpoll)

    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error)#处理异常
    def handle_error(self, failure):
        # 处理异步插入的异常
        print(failure)
    def do_insert(self, cursor, item):
        # 执行具体的插入
        insert_sql = """
                    insert into jobbole_article
                    (title,create_date,url,url_object_id,praise_nums,comment_nums,fav_nums,tags,front_image_url,content)
                    values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """
        cursor.execute(insert_sql, (
        item["title"], item["create_date"], item["url"], item["url_object_id"], item["praise_nums"],
        item["comment_nums"], item["fav_nums"], item["tags"], item["front_image_url"], item["content"]))
