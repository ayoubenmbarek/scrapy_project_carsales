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
import json
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.webdriver.common.by import By
class immomexiqueSpider(scrapy.Spider):
        name = "immomexiquespider3"
        handle_httpstatus_list = [301, 302, 200]#, 500]#, 403]
	allowed_domains = ['inmuebles24.com']
	#sudo docker run -p 5023:5023 -p 8050:8050 -p 8051:8051 scrapinghub/splash
	#start_urls = ['http://www.inmuebles24.com/inmuebles-en-venta.html']
	start_urls = ['http://www.inmuebles24.com/propiedades/pent-house-b-nayar-4-recamaras-52629200.html'#,
	               #'http://www.inmuebles24.com/casas-o-duplex-o-casa-en-condominio-en-venta.html',
	               #'http://www.inmuebles24.com/terrenos-en-venta.html',
	               ##'http://www.inmuebles24.com/oficinas-en-venta.html',
	               #'http://www.inmuebles24.com/nave-industrial-o-bodega-galpon-o-bodegas-comerciales-en-venta.html',
	               #'http://www.inmuebles24.com/otros-tipos-de-propiedades-en-venta.html'
	               ]
	download_delay = 0
	#setting user agent in chrome
	#from selenium.webdriver.chrome.options import Options
        #opts = Options()
        #opts.add_argument("user-agent=whatever you want")
        #driver = webdriver.Chrome(chrome_options=opts)
        #ua  = random.choice(settings.get('USER_AGENT_LIST'))
        #user_agent_list = settings.getUSER_AGENT_LIST
        #if ua:
               # opts = Options()
               # opts.add_argument(ua)
	       # driver = webdriver.Chrome(chrome_options=opts)
        #for user_agent in user_agent_list:
                #opts = Options()
                #opts.add_argument("user-agent=user_agent")
	        #driver = webdriver.Chrome(chrome_options=opts)

        def start_requests(self):
                script = """
                function main(splash)
                    local url = splash.args.url
                    assert(splash:go(url))
                    assert(splash:wait(1))

                    assert(splash:runjs('document.getElementsByTagName("span")[2].click()'))
                    assert(splash:wait(1))

                    -- return result as a JSON object
                    return {
                        html = splash:html()
                    }
                end
                """
                for url in self.start_urls:
                    yield scrapy.Request(url, self.parse_result, meta={
                        'splash': {
                            'args': {'lua_source': script},
                            'endpoint': 'execute',
                        }
                    })
            
        def parse_result(self, response):
                myItem = ImmomesxiqueItem()
                # fetch base URL because response url is the Splash endpoint
                #baseurl = response.meta["_splash_processed"]["args"]["url"]

                # decode JSON response
                #myItem["listing_page"] = json.loads(response.body_as_unicode())
                myItem["listing_page"] = response.body
                yield myItem

                # and build a new selector from the response "html" key from that object
                #selector = scrapy.Selector(text=splash_json["html"], type="html")
	
	
