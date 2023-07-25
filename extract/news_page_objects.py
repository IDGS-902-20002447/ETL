from bs4 import BeautifulSoup
from urllib.request import Request,urlopen
from common import config



#Creamos una clase general
class NewsPage:
    def __init__(self,news_site_uid,url):
        #Obtenemos una referencia a la configuracion
        self._config=config()['news_sites'][news_site_uid]
        self._queries=self._config['queries']
        self._html=None

        self._visit(url)

    
    #Metodo para ejecutar una consulta en el arbol html
    def _select(self,query_string):
        return self._html.select(query_string)


    #Cuando no viene con cabecera las pagias piensan que es un ataque 
    # por lo que se REQUIERE la cabecer y la toma com peticion valida
    def _visit(self,url):
         #Definimos las cabeceras de la peticion
         hdr={'User-Agent':'Mozila/5.0'}

         #Hacemos la peticion
         request=Request(url,headers=hdr)

         #Abrims la pagia 
         response=urlopen(request)

         #Creamos el objeto BeautifoulSOpup
         self._html=BeautifulSoup(response.read(),'html.parser')



#Creamos una clase que representa a pagina principal del sitio de noticias.
class HomePage(NewsPage):
    def __init__(self,news_site_uid,url):
        super().__init__(news_site_uid, url)


    def __init__(self,news_site_uid,url):
        #Obtenemos una referencia a la configuracion
        self._config=config()['news_sites'][news_site_uid]
        self._queries=self._config['queries']
        self._html=None

        self._visit(url)

    #Definimos una propiedad que obtiene la lista de enlaces recuperados por la consulta
    @property
    def article_links(self):
        link_list=[]
        #Se sacan todos los enlaces
        for link in self._select(self._queries['homepage_article_links']):
            if link and link.has_attr('href'):
                link_list.append(link)

        #Retornamos la lista evitando repetidos
        return set(link ['href'] for link in link_list)


class ArticlesPage(NewsPage):
    def __init__(self, news_site_uid, url):
        self._url=url
        super().__init__(news_site_uid, url)

    #Definimos una ppropiedad para recuperar el titulo del articulo
    @property
    def title(self):
        result = self._select(self._queries['article_title'])
        return result[0].text if len(result) else ''
    
    #Definimos una ppropiedad para recuperar el cuerpo del articulo
    @property
    def body(self):
        result = self._select(self._queries['article_body'])
        return result[0].text if len(result) else ''
    
    #Definimos una ppropiedad para recuperar la url del articulo
    @property
    def url(self):
        return self._url
    
 