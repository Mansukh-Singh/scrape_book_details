from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from functions import books,mongo_db
import logging

logging.basicConfig(filename='scrapper.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)
driver.get("https://toscrape.com/")

element = wait.until(EC.presence_of_element_located((By.LINK_TEXT, "books.toscrape.com")))
element.click()

#book_type = driver.find_element(By.LINK_TEXT,"Music")
book_class = wait.until(EC.element_to_be_clickable((By.LINK_TEXT,"Music")))
book_class.click()

page_source = driver.page_source

soup = BeautifulSoup(page_source,'html.parser')

books_info = soup.find_all("li",class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")

book_array = []
logger.info("Scrapping data from the url")
for book_info in books_info:
    book_dictionary = books(book_info)
    book_array.append(book_dictionary)

mongo_db(book_array)

driver.quit()
