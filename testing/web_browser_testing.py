from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# Using Chrome to access web
driver = webdriver.Chrome('/Users/awd/Library/Mobile Documents/com~apple~CloudDocs/PycharmProjects/A-Level-AQA-CS/testing/chromedriver')

sites = ['https://www.shiplake.org.uk', 'https://www.bbc.co.uk']

# Open the website

for s in sites:
    driver.execute_script("window.open('" + s + "', '_blank')")



driver.close()