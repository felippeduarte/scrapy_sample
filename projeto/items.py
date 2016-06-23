# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class LojaItem(Item):
    #necessario para download de imagens
    image_urls = Field()
    images = Field()    

    nomeProduto = Field()
    descricaoProduto = Field()
    nomeCategoria = Field()
    preco = Field()
    link = Field()
    idLoja = Field()