import scrapy
from scrapy import Request
from immomesxique.items import ImmomesxiqueItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import ast
from scrapy_splash import SplashRequest
from datetime import datetime  
from datetime import timedelta 
#make a change to test jenkins
from selenium import webdriver
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.webdriver.common.by import By
class immomexiqueSpider(scrapy.Spider):
        name = "immomexiquespider26"
        handle_httpstatus_list = [301, 302, 200]#, 500]#, 403]
	allowed_domains = ['inmuebles24.com']
	#sudo docker run -p 5023:5023 -p 8050:8050 -p 8051:8051 scrapinghub/splash
	#start_urls = ['http://www.inmuebles24.com/inmuebles-en-venta.html']
	start_urls = ['http://www.inmuebles24.com/departamentos-en-venta.html'#,
	               #'http://www.inmuebles24.com/casas-o-duplex-o-casa-en-condominio-en-venta.html',
	               #'http://www.inmuebles24.com/terrenos-en-venta.html',
	               ##'http://www.inmuebles24.com/oficinas-en-venta.html',
	               #'http://www.inmuebles24.com/nave-industrial-o-bodega-galpon-o-bodegas-comerciales-en-venta.html',
	               #'http://www.inmuebles24.com/otros-tipos-de-propiedades-en-venta.html'
	               ]
	download_delay = 0
	
	def parse(self, response):
	
                #myItem = ImmomesxiqueItem()        
                container = response.css('li.post.destacado')
                for link in container:
		      myItem = ImmomesxiqueItem() 	
                      myItem["listing_page"] = response.url  
                      url = link.css('a.dl-aviso-link ::attr(href)').extract_first()
                      full_url = response.urljoin(url)
                      request = scrapy.Request(full_url, callback=self.second_page)#, dont_filter=True) 
                      request.meta['myItem'] = myItem
                      yield request
                      #scrapy.Request(
                         ##   'http://example.com',
                           # headers={
                               # 'X-Crawlera-Max-Retries': 1,
                               # ...
                            #},
                        #)
                #for i in range(2,15)         :
                        #next_page = 'http://www.inmuebles24.com/departamentos-en-venta-pagina-'+str(i)+'.html'
                        #yield scrapy.Request(
                            #next_page)
                linkcontainer = response.css('li.pagination-action-next')
                for cc in linkcontainer:
                        next_page = cc.css('a ::attr(href)').extract_first()
                        if next_page:
                            next = response.urljoin(next_page)
                            yield SplashRequest(
                            next)#, callback=self.parse)
		
	        #next_page = response.css('a.more-products-btn.has-infinite ::attr(href)').extract_first()
                #if next_page:
                    #yield scrapy.Request(
                        #response.urljoin(next_page))#,callback=self.parse)                      
                
        def second_page(self, response):
                hxs = Selector(response)
                myItem = response.meta["myItem"]  
                myItem["Site"] = 'inmuebles24.com'
                myItem["ANNONCE_LINK"] = response.url
                d = myItem["ANNONCE_LINK"].split('.html')
                dd = d[0]
                ddd = dd.split('-')
                myItem["ID_CLIENT"] = ddd[-1]
                

                #driver = webdriver.Chrome()
                #driver.get(myItem["ANNONCE_LINK"])
                
                ##click_phone = driver.find_element_by_css_selector('.btn-phone')
                #click_phone = driver.find_element(By.XPATH, "//button[@class='btn-phone']")
                #click_phone.click()
                #myItem["AGENCE_TEL"] = driver.find_element(By.XPATH, "//span[@class='lead-phone']").text
                #codigo = driver.find_element(By.XPATH, "//p[@class='more-data']/b").text
                #myItem["AGENCE_CONTACT"] = driver.find_element(By.XPATH, "//p[2][@class='more-data']/b").text
                #driver.find_element_by_css_selector('span.lead-phone').text
                #driver.Quit()
                #driver.quit()
                #driver.start()
                #LOGGER.setLevel(logging.WARNING)
                myItem["FROM_SITE"] = 'inmuebles24'
                all_span = response.css('span.valor ::text').extract()
                all_text = all_span[2]
                cut = all_text.split(':')
                #myItem["ID_CLIENT"] = cut[-1] 
                #try:
                   #     all_text_date = all_span[3]
                      #  all_text_date_cut = all_text_date.split(' ')
                       # number_days = all_text_date_cut[-2]
                        #number_days_int = int(number_days)
                        #myItem["ANNONCE_DATE"] = datetime.now() - timedelta(days=number_days_int)  
                        #myItem["ANNONCE_DATE"] = datetime.date.today() - timedelta(days=number_days_int)
                #except:
                        #pass  
                bb = response.xpath('//*[@id="idAviso"]/@value').extract() #continue it
                a = bb[-1]
                a1 = a.split(' ')
                date = a1[11]
                date1 = date.split('=')
                myItem["ANNONCE_DATE"] = date1[-1] # or response.xpath("//span[contains(text(), 'Entrega')]/following-sibling::span/text()").extract()

                myItem["CATEGORIE"] = response.xpath('//*[@class="nombre"]/text()').extract()[1] #or #response.xpath("//span[contains(text(), 'Tip')]/following-sibling::span/text()").extract()

                #myItem["NEUF_IND"] =
                myItem["NOM"] = response.css('title ::text').extract_first()
                myItem["ADRESSE"] = response.xpath('//*[@id="map"]/div[1]/div/ul/li/text()').extract()
                items = response.xpath('//script/text()').re(".*tipoDeOperacion.*")
                st = items[0]
                new = st.split('push')
                new1 = new[-1]
                new_dict = new1.split(';')
                new_dict1 = new_dict[0]
                new_dict2 = ast.literal_eval(new_dict1)
                myItem["PRIX"] = new_dict2.get('precioVenta') #or response.xpath("//span[contains(text(), 'Pr')]/following-sibling::span/text()").extract()
                #myItem["CP"] =
                myItem["VILLE"] = new_dict2.get('ciudad')
                myItem["QUARTIER"] = new_dict2.get('barrio')
                #myItem["DEPARTEMENT"] =
                #myItem["REGION"] =
                myItem["PROVINCE"] = new_dict2.get('provincia')
                myItem["ACHAT_LOC"] = new_dict2.get('tipoDeOperacion')#1
                myItem["MAISON_APT"] = new_dict2.get('tipoDePropiedad')#1
                myItem["ANNONCE_TEXT"] = response.css('span.js-flex-box.description-body ::text ').extract_first()
                #myItem["ANNONCE_TEXT"] = response.xpath('//*[@id="id-descipcion-aviso"]/text()').extract()
                #myItem["ETAGE"] =
                #myItem["NB_ETAGE"] =
                myItem["LATITUDE"] = response.xpath('//*[@id="lat"]/@value').extract()
                myItem["LONGITUDE"] = response.xpath('//*[@id="lng"]/@value').extract()
                #response.xpath("//span[contains(@class, 'nombre') and text() = 'T']//following-sibling::span/text()").extract()
                try:
                        for bb in response.css('div.card.aviso-datos'):
                                all_s = bb.css('span.nombre ::text').extract()
                                myItem["M2_TOTALE"] = all_s[4] #or response.xpath("//li/span[contains(@class, 'nombre')]/text()").extract()[4]
                                myItem["SURFACE_TERRAIN"] = all_s[7] #response.xpath("//li/span[contains(@class, 'nombre')]/text()").extract()[6]
                except:
                        pass
                #myItem["NB_GARAGE"] =
                #myItem["PHOTO"] = response.xpath('/html/head/meta[10]/@content').extract()
                id_annonce = response.xpath('//span[contains(text(), "del anun")]/text()').extract_first()
                id1 = id_annonce.split(':')
                myItem["MINI_SITE_ID"] = id1[-1]
                #myItem["PIECE"] =
                
                #myItem["PRIX_M2"] =
                #myItem["URL_PROMO"] =
                #myItem["PAYS_AD"] =
                #myItem["PRO_IND"] =
                #myItem["SELLERTYPE"] =
                #myItem["MINI_SITE_URL"] =
                myItem["AGENCE_NOM"] = response.css('span.h3.pull-left.datos-inmobiliaria-title ::text').extract()
                #myItem["AGENCE_ADRESSE"] =
                #myItem["FLUX"] =
                #myItem["SITE_SOCIETE_URL"] =
                #myItem["SITE_SOCIETE_ID"] =
                #myItem["SITE_SOCIETE_NAME"] =
                #myItem["AGENCE_RCS"] =
                #myItem["SPIR_ID"] =
                #myItem["AGENCE_VILLE"] =
                #myItem["AGENCE_DEPARTEMENT"] =
                #myItem["EMAIL"] =
                #myItem["WEBSITE"] =
                #myItem["AGENCE_TEL"] = response.css('span.lead-phone ::text').extract()
                #myItem["AGENCE_TEL_2"] =
                #myItem["AGENCE_TEL_3"] =
                #myItem["AGENCE_TEL_4"] =
                #myItem["AGENCE_FAX"] =
                #myItem["AGENCE_CONTACT"] =
                #myItem["PAYS_DEALER"] =
                
                
                yield myItem


