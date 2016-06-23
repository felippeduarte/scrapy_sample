from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from tutorial.items import LojaItem

class supermercadocasagrandeSpider(CrawlSpider):
    name = "supermercadocasagrande"
    allowed_domains = ['www.supercasagrande.com.br']
    start_urls = [
        "http://www.supercasagrande.com.br/?content=estoque"
    ]
    rules = (
        Rule(SgmlLinkExtractor(allow=['/?content=detalhar&id=\d+']), 'parseItem'),
        Rule(SgmlLinkExtractor(allow=['/?coluna=\d+&content=estoque']))
    )

    
    def parseItem(self, response):
        hxs = HtmlXPathSelector(response)
        item = LojaItem()
        
        item['preco'] = hxs.select('//span[@class="dstq_txt_nome"][2]/text()').re('[0-9]+[\.|,]?[0-9]*')
        if len(item['preco']) > 0:
            item['preco'] = item['preco'][0].replace(",",".")
        else:
            return
        
        item['image_urls'] = ['http://www.supercasagrande.com.br/' + 
                              hxs.select('//div[@id="previewPane"]/img/@src').extract()[0]]
        item['nomeProduto'] = (hxs.select('//span[@class="dstq_txt_marca"]/text()').extract()[0] +
                             " " + 
                             hxs.select('//span[@class="dstq_txt_nome"][1]/text()').extract()[0].
                             replace("Marca: ", "")).strip()
        item['descricaoProduto'] = hxs.select('//span[@class="dstq_txt_desc"]/text()').extract()
        
        if len((item['descricaoProduto'])) > 0:
            item['descricaoProduto'] = item['descricaoProduto'][0].strip()
        else:
            item['descricaoProduto'] = ''
            
        item['nomeCategoria'] = ''
        item['link'] = response.url
        item['idLoja'] = '2'
        
        return item
