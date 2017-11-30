import scrapy
from scrapy import Request
from immomesxique.items import ImmomesxiqueItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import ast
from scrapy.conf import settings
from scrapy_splash import SplashRequest
from datetime import datetime  
from datetime import timedelta 
from selenium import webdriver
from ..settings import USER_AGENT_LIST
import random
import time
from scrapy.http.request import Request
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.webdriver.common.by import By
class immomexiqueSpider(scrapy.Spider):
        name = "immomexiquespider2809"
        handle_httpstatus_list = [301, 302, 200]#, 500]#, 403]
	allowed_domains = ['inmuebles24.com']
	#sudo docker run -p 5023:5023 -p 8050:8050 -p 8051:8051 scrapinghub/splash
	#start_urls = ['http://www.inmuebles24.com/inmuebles-en-venta.html']
	start_urls = [ 'http://www.inmuebles24.com/departamentos-en-venta.html',
	               'http://www.inmuebles24.com/casas-o-duplex-o-casa-en-condominio-en-venta.html',
	               'http://www.inmuebles24.com/terrenos-en-venta.html',
	               'http://www.inmuebles24.com/oficinas-en-venta.html',
	               'http://www.inmuebles24.com/nave-industrial-o-bodega-galpon-o-bodegas-comerciales-en-venta.html',
	               'http://www.inmuebles24.com/otros-tipos-de-propiedades-en-venta.html'
	               ]
	download_delay = 0
	#setting user agent in chrome
	#from selenium.webdriver.chrome.options import Options
        #opts = Options()
        #opts.add_argument("user-agent=whatever you want")
        #driver = webdriver.Chrome(chrome_options=opts)
        #user_agent_list = settings.getUSER_AGENT_LIST
        #ua  = random.choice(settings.get('USER_AGENT_LIST'))
        #if ua:
               # opts = Options()
                #opts.add_argument(ua)
	        #driver = webdriver.Chrome(chrome_options=opts)
	        
        #def start_requests(self):

                #headers = {
                       # "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                        #"Accept-Encoding":"gzip, deflate, sdch",
                        #"Accept-Language":"fr-FR,fr;q=0.8,en-US;q=0.6,en;q=0.4",
                       # "Cache-Control":"no-cache",
                       # "Connection":"keep-alive",
                       # "Cookie":"__uzma=ced3ae0c-caaf-4bf2-ba87-728b9da6d9a13771; __uzmb=1504019773; __ssds=2; _hjIncludedInSample=1; mousestats_vi=5f7c6e368438db666705; IDusuario=53208670; G_ENABLED_IDPS=google; __atuvc=5%7C35%2C0%7C36%2C13%7C37%2C0%7C38%2C14%7C39; listado-precio-promedio=false; _gu=1220143e-9a46-4a0e-a389-21efee696fef; _gs=2.s(src=http://www.inmuebles24.com/?landingHome=Venta)c[Desktop,Chrome,134:,Linux/Unix,41.226.248.83]; _gw=2.221530(sc~3,s~owvpby)221819(sc~m,s~owzcyo)u[~0,~0,~0,~0,~0]v[~ey6td,~1,~1]a(); __ssuzjsr2=a9be0cd8e; _ga=GA1.2.583051268.1504019655; _gid=GA1.2.530395585.1506414110; __uzmc=7776530497592; __uzmd=1506587146; sessionId=c612a3c5-092d-4446-b83d-cefa7de88615",
                       # "Host":"www.inmuebles24.com",
                       # "Pragma":"no-cache",
                       # "Upgrade-Insecure-Requests":"1",
                      # "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
                #}
#
               # yield Request(url= 'http://www.inmuebles24.com/departamentos-en-venta.html', callback=self.parse, headers=headers)

	        
	def parse(self, response):
	
                #myItem = ImmomesxiqueItem()    
                container = response.css('h4.post-titulo')    
                #container = response.css('li.post.destacado')
                #self.driver = webdriver.Chrome()
                
                for link in container:
		      myItem = ImmomesxiqueItem() 	
                      myItem["listing_page"] = response.url 
                       
                      url = link.css('a ::attr(href)').extract_first()
                      
                      #url = link.css('a.dl-aviso-link ::attr(href)').extract_first()
                      full_url = response.urljoin(url)
                      request = scrapy.Request(full_url, callback=self.second_page)#, meta={
                                #'splash': {
                                  #  'endpoint': 'render.html',
                                   # 'args': {'wait': 0.5}
                                #}
                            #})#, dont_filter=True) 
                      
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
                        #yield scrapy.Request(next_page)
                        
                #linkcontainer = response.css('li.pagination-action-next')
                #for cc in linkcontainer:
                      #  next_page = cc.css('a ::attr(href)').extract_first()
                       # if next_page:
                        #    next = response.urljoin(next_page)
                          #  yield scrapy.Request(
                            #next)#, meta={
                                #'splash': {
                                  #  'endpoint': 'render.html',
                                   # 'args': {'wait': 0.5}
                                #}
                            #})#, callback=self.parse)
		
	        #next_page = response.css('a.more-products-btn.has-infinite ::attr(href)').extract_first()
	        next_page = response.css('li.pagination-action-next > a ::attr(href)').extract_first()
                if next_page:
                    yield scrapy.Request(
                        response.urljoin(next_page))#,callback=self.parse)                      
                
        def second_page(self, response):
                hxs = Selector(response)
                myItem = response.meta["myItem"]
                #while 1==1:
                #driver = webdriver.Chrome()
                #while True:
                myItem["ANNONCE_LINK"] = response.url
                #self.driver.get(myItem["ANNONCE_LINK"])
                
                ##click_phone = driver.find_element_by_css_selector('.btn-phone')
                #click_phone = self.driver.find_element(By.XPATH, "//button[@class='btn-phone']")
                #click_phone.click()
                #myItem["AGENCE_TEL"] = self.driver.find_element(By.XPATH, "//span[@class='lead-phone']").text
                #codigo = self.driver.find_element(By.XPATH, "//p[@class='more-data']/b").text
                #myItem["AGENCE_CONTACT"] = self.driver.find_element(By.XPATH, "//p[2][@class='more-data']/b").text
                #if "captcha" in response.body:
                       # time.sleep(5)
                #self.driver.back()
                #myItem = response.meta["myItem"]  
                myItem["Site"] = 'inmuebles24.com'
                d = myItem["ANNONCE_LINK"].split('.html')
                dd = d[0]
                ddd = dd.split('-')
                myItem["ID_CLIENT"] = ddd[-1]
                
                #while True:
                #driver = webdriver.Chrome()
                 
                ##driver.find_element_by_css_selector('span.lead-phone').text
                ##driver.Quit()
                #self.driver.close()
                #self.driver.quit()
                 
                #pass

                ##driver.start()
                #LOGGER.setLevel(logging.WARNING)
                myItem["FROM_SITE"] = 'inmuebles24'
                #all_span = response.css('span.valor ::text').extract()
                #all_text = all_span[2]
                #cut = all_text.split(':')
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
                try:
                        bb = response.xpath('//*[@id="idAviso"]/@value').extract() #continue it
                        a = bb[-1]
                        a1 = a.split(' ')
                        date = a1[11]
                        date1 = date.split('=')
                        myItem["ANNONCE_DATE"] = date1[-1] # or response.xpath("//span[contains(text(), 'Entrega')]/following-sibling::span/text()").extract()
                except:
                        pass
                try:
                        myItem["CATEGORIE"] = response.xpath('//*[@class="nombre"]/text()').extract()[1] #or #response.xpath("//span[contains(text(), 'Tip')]/following-sibling::span/text()").extract()
                        #myItem["CATEGORIE"] = response.xpath("//span[contains(text(), 'Tip')]/following-sibling::span/text()").extract()
                except:
                        pass

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
                myItem["AGENCE_NOM"] = response.css('span.h3.pull-left.datos-inmobiliaria-title ::text').extract()
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
                #pass
                #self.driver.back()
                yield myItem


