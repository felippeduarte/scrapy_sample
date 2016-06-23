from scrapy import log
from scrapy.exceptions import DropItem
from twisted.enterprise import adbapi
from tutorial.items import LojaItem

import time
import MySQLdb
import MySQLdb.cursors
import json

class MySQLStorePipeline(object):

    def __init__(self):
        # @@@ hardcoded db settings
        # TODO: make settings configurable through settings
        self.dbpool = adbapi.ConnectionPool('MySQLdb',db='scrapy',user='root',passwd='senha1',cursorclass=MySQLdb.cursors.DictCursor,charset='utf8',use_unicode=True)

    def process_item(self, item, spider):

        # run db query in thread pool
        if isinstance(item, LojaItem) is True:
            query = self.dbpool.runInteraction(self._conditional_insert,item)
        return item

    def _conditional_insert(self, tx, item):
        # create record if doesn't exist. 
        # all this block run on it's own thread
        tx.execute("select * from scrapy.Estagiamento where link = %s", (item['link']))

        imagem = ''

        if len(item['images']) > 0:
            imagem = item['images'][0]['path'].replace('full/','')

        result = tx.fetchone()
        if result:
            tx.execute(\
                "update scrapy.estagiamento set nomeProduto=%s, descricaoProduto=%s, nomeCategoria=%s, preco=%s, imagem=%s, idLoja=%s, horario=NOW() "
                "where link=%s",
                (item['nomeProduto'],
                 item['descricaoProduto'],
                 item['nomeCategoria'],
                 item['preco'],
                 imagem,                 
                 item['idLoja'],
                 item['link'])
            )
            log.msg("Item ja existe; atualizando: %s" % item, level=log.DEBUG)
        else:
            tx.execute(\
                "insert into scrapy.estagiamento (nomeProduto, descricaoProduto, nomeCategoria, preco, link, imagem,  horario, idLoja) "
                "values (%s, %s, %s, %s, %s, %s, NOW(), %s)",
                (item['nomeProduto'],
                 item['descricaoProduto'],
                 item['nomeCategoria'],
                 item['preco'],
                 item['link'],
                 imagem,
                 item['idLoja'])
            )
            log.msg("Item incluido: %s" % item, level=log.DEBUG)
            
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.http import Request

class ImagemPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Imagem nao encontrada")
        item['image_paths'] = image_paths
        return item