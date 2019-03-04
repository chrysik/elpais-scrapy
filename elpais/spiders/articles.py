import scrapy
import re

class GetArticlesSpider(scrapy.Spider):
	name = 'elpaisarticles'

	def start_requests(self):
		urls = []
		for i in range(1,5000):
			urlpage = "https://elpais.com/tag/cataluna/a/{0}".format(str(i))
			yield scrapy.Request(url=urlpage, callback=self.geturls)

	def geturls(self,response):
		for article in response.css('article.articulo'):
			url = "https:{0}".format(article.css('a::attr(href)').extract_first())
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self,response):
		author = response.css('span.autor-nombre')
		author = author.css('a::text').extract_first()

		mainarticle = []
		main = response.css('div.articulo-cuerpo')
		for p in main.css('p::text').extract():
			mainarticle.append(p)
		mainarticle =' '.join(mainarticle)

		localization = response.css('span.articulo-localizacion::text').extract_first()

		mydict = {	'id' : re.search("(?<=/)(?!.*/)(.*)(?=_)",response.request.url).group(0),
					'url' : response.request.url,
					'title' : response.css('h1.articulo-titulo::text').extract_first(),
					'subtitle' : response.css('h2.articulo-subtitulo::text').extract_first(),
					'author' : author,
					'localization' : localization,
					'datetime' : response.css('time.articulo-actualizado::attr(datetime)').extract_first(),
					'mainarticle' : mainarticle
					}
		for key in mydict:
			try:
				for char in ["\n","\t",";"]:
					mydict[key] = mydict[key].replace(char," ")
				mydict[key] = ' '.join(mydict[key].split())
			except:
				pass

		yield mydict

