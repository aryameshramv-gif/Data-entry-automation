import time
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import lxml
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os

load_dotenv()

# URLS
ZILLOW_URL = "https://appbrewery.github.io/Zillow-Clone/"
FORMS_URL = os.getenv("FORM_URL")

# BS4 SET UP
header = {
    "Accept-Language": "en-US,en;q=0.9,en-IN;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0",
}
response = requests.get(url=ZILLOW_URL, headers=header)
zillow_html = response.text

# WEBSITE SCARPING
soup = BeautifulSoup(zillow_html, "lxml")

link_list = []
price_list = []
address_list = []

for listing in soup.find_all(class_="StyledPropertyCardDataWrapper"):
    # price
    price = listing.find(class_="PropertyCardWrapper__StyledPriceLine").getText().strip('+/mo')
    price_list.append(price.replace("+ 1bd"," "))
    # link
    link = listing.find(class_="StyledPropertyCardDataArea-anchor").get("href")
    link_list.append(link)
    # address
    address = listing.find('address', {'data-test': 'property-card-addr'}).getText().strip()
    address_list.append(address)

print(price_list)
print(link_list)
print(address_list)

# SELENIUM SET UP
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
driver.get(FORMS_URL)

# FORM FILLING
inputs = 0
required_inputs = len(address_list)
print(required_inputs)
print(inputs)

while inputs != required_inputs:
    address_input = driver.find_element(By.XPATH,
                                        "//*[@id='mG61Hd']/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input")
    address_input.send_keys(address_list[inputs])
    price_input = driver.find_element(By.XPATH,
                                      "//*[@id='mG61Hd']/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input")
    price_input.send_keys(price_list[inputs])
    link_input = driver.find_element(By.XPATH,
                                     "//*[@id='mG61Hd']/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input")
    link_input.send_keys(link_list[inputs])

    submit_button = driver.find_element(By.CSS_SELECTOR, ".NPEfkd.RveJvd.snByac")
    submit_button.click()

    another_response = driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div[1]/div/div[4]/a")
    another_response.click()

    inputs += 1