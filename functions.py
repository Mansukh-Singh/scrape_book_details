import requests
from bs4 import BeautifulSoup
from constants import client
import logging

logging.basicConfig(filename='scrapper.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

def books(name):
    book_details = {}
    url_name = name.find('h3').find('a')['href'].split('/')[3]
    url = f"http://books.toscrape.com/catalogue/{url_name}/index.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    book_name = soup.find('div',class_='col-sm-6 product_main').find('h1').text
    book_price = soup.find('div',class_='col-sm-6 product_main').find('p',class_='price_color').text[1:]
    book_rating = soup.find('div',class_='col-sm-6 product_main').find('p',class_='star-rating')['class'][1]
    book_instock_availability = soup.find('div',class_='col-sm-6 product_main').find('p',class_='instock availability').text.strip('\n ')
    book_upc = soup.find('table',class_='table table-striped').find('td').text
    book_description = soup.find('p',class_=False,id=False).text
    book_details['Book Name'] = book_name
    book_details['Book Price'] = book_price
    book_details['Book Rtaing'] = book_rating
    book_details['Book Instock Availability'] = book_instock_availability
    book_details['Book UPC'] = book_upc
    book_details['Book Description'] = book_description
    return book_details

def mongo_db(data):
    try:
        db = client["myScrape"]
        collection = db["mycollection"]
        result = collection.insert_many(data)
        logger.info("Data inserted into MongoDB")
    except Exception as e:
        logger.info(f"An error occured: {e}")
    pass