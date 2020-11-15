import scrapy
import json
import os

class BoeSpider(scrapy.Spider):
    name = "boe_spider"
    start_urls = [f"https://boe.es/boe/dias/2020/11/{day}/" for day in ['03','04', '05', '06', '07', '09', '10', '11', '12', '13', '14']]
    
    def parse(self, response):
        for dispo in response.css(".puntoHTML > a::attr('href')").extract():
            url = response.urljoin(dispo).replace('/txt.php', '/xml.php') 
            yield scrapy.Request(url, callback=self.save_xml_dispo)

    def save_xml_dispo(self, response):
        tags = {
            "documento" : response.xpath("//documento/text()").extract_first(),
            "metadatos" : response.xpath("//metadatos/text()").extract_first(),
            "identificador" : response.xpath("//identificador/text()").extract_first(),
            "titulo" : response.xpath("//titulo/text()").extract_first(),
            "diario" : response.xpath("//diario/text()").extract_first(),
            "diario_numero" : response.xpath("//diario_numero/text()").extract_first(),
            "seccion" : response.xpath("//seccion/text()").extract_first(),
            "subseccion" : response.xpath("//subseccion/text()").extract_first(),
            "departamento" : response.xpath("//departamento/text()").extract_first(),
            "rango" : response.xpath("//rango/text()").extract_first(),
            "numero_oficial" : response.xpath("//numero_oficial/text()").extract_first(),
            "fecha_disposicion" : response.xpath("//fecha_disposicion/text()").extract_first(),
            "fecha_publicacion" : response.xpath("//fecha_publicacion/text()").extract_first(),
            "fecha_vigencia" : response.xpath("//fecha_vigencia/text()").extract_first(),
            "fecha_derogacion" : response.xpath("//fecha_derogacion/text()").extract_first(),
            "letra_imagen" : response.xpath("//letra_imagen/text()").extract_first(),
            "pagina_inicial" : response.xpath("//pagina_inicial/text()").extract_first(),
            "pagina_final" : response.xpath("//pagina_final/text()").extract_first(),
            "suplemento_letra_imagen" : response.xpath("//suplemento_letra_imagen/text()").extract_first(),
            "suplemento_pagina_inicial" : response.xpath("//suplemento_pagina_inicial/text()").extract_first(),
            "suplemento_pagina_final" : response.xpath("//suplemento_pagina_final/text()").extract_first(),
            "estatus_legislativo" : response.xpath("//estatus_legislativo/text()").extract_first(),
            "origen_legislativo" : response.xpath("//origen_legislativo/text()").extract_first(),
            "estado_consolidacion" : response.xpath("//estado_consolidacion/text()").extract_first(),
            "judicialmente_anulada" : response.xpath("//judicialmente_anulada/text()").extract_first(),
            "vigencia_agotada" : response.xpath("//vigencia_agotada/text()").extract_first(),
            "estatus_derogacion" : response.xpath("//estatus_derogacion/text()").extract_first(),
            "url_epub" : response.xpath("//url_epub/text()").extract_first(),
            "url_pdf" : response.xpath("//url_pdf/text()").extract_first(),
            "url_pdf_catalan" : response.xpath("//url_pdf_catalan/text()").extract_first(),
            "url_pdf_euskera" : response.xpath("//url_pdf_euskera/text()").extract_first(),
            "url_pdf_gallego" : response.xpath("//url_pdf_gallego/text()").extract_first(),
            "url_pdf_valenciano" : response.xpath("//url_pdf_valenciano/text()").extract_first(),
            "analisis" : response.xpath("//analisis/text()").extract_first(),
            "notas" : response.xpath("//notas/text()").extract_first(),
            "materias" : response.xpath("//materias/text()").extract_first(),
            "alertas" : response.xpath("//alertas/text()").extract_first(),
            "referencias" : response.xpath("//referencias/text()").extract_first(),
            "anteriores" : response.xpath("//anteriores/text()").extract_first(),
            "posteriores" : response.xpath("//posteriores/text()").extract_first(),
            "texto" : response.xpath("//texto").extract_first(),
        }
        path = f"../data/{tags['fecha_publicacion']}/{tags['seccion']}/{tags['subseccion']}/{tags['departamento']}"
        filename = f"{tags['identificador']}.json" 
        os.makedirs(path, exist_ok=True)
        with open(f"{path}/{filename}", "w") as file:
            json.dump(tags, file)
