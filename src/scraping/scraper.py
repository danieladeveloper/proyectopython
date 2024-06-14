import requests #importar el modulo request para hacer las solicitudes HTTP
from bs4 import BeautifulSoup #para analizar los documentos HTML
import pandas as pd  #para manejar los dataframes

def fetch_page(url):
    """ obtener contenido de una pag""" 
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"failed to fetch page: {url}")

base_url="https://lee.com.ec/product-category/descuentos-on-line/"

def parse_product(product):
    title= product.find("h2",class_="woocommerce-loop-product__title").text.strip() #obtener el título del producto
    price=0
    promo=0
    
    #print(len(product.select("span.price")))
    #print("----------------------")
    if len(product.select("span.price")) > 0:
        price= product.select("bdi")[0].get_text()
        #price= precioa.replace("$","").strip()
        promo= product.select("bdi")[1].get_text()
        #promo= promoa.replace("$","").strip()
    
    return{
        "title": title,
        "price": price,
        "promo": promo,
    }

    
def scrape(url):
    page_content= fetch_page(url)
    soup= BeautifulSoup(page_content, "html.parser")
    products = soup.find_all("li", class_="product")
    products_data=[] #almacena los datos de los productos
    
    for product in products:
        product_info=parse_product(product)
        products_data.append(product_info)

    return products_data


def obtener_datos_todas_paginas(base_url):
  productos=[]
  page=1
  while True:
    url = f"{base_url}?product-page={page}"
    nuevos_productos = scrape(url)
    #print(nuevos_productos)
    if not nuevos_productos:
      break
    productos.extend(nuevos_productos)
    page += 1
  return productos


productosArray=obtener_datos_todas_paginas(base_url)


pf = pd.DataFrame(productosArray)
pf.to_csv('data/raw/products.csv', index=False)

