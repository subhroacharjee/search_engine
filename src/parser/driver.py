
import os, re
from click import pass_context
from selenium import webdriver

from src.utils.env import cwd_path

class Driver:
    def __init__(self):
        pass
    
    @staticmethod
    def get_driver():
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument('--headless')
        driver = webdriver.Chrome(os.path.join(cwd_path(),'chromedriver'), chrome_options=options)
        return driver
    @staticmethod
    def close_driver( driver):
        driver.close()
    
    @staticmethod
    def get_website_data(url):
        '''
        Gets website title, description, urls and content
        '''
        driver = Driver.get_driver()
        try:
            driver.get(url)
            title = driver.title
            urls = []
            hyperlinks = driver.find_elements_by_tag_name("a")

            #hyperlinks for urls
            for i in hyperlinks:
                urls.append(i.get_attribute('href'))
            meta_tags = driver.find_elements_by_tag_name("meta")
            description = ""

            # getting description from meta tag
            for meta in meta_tags:
                if meta.get_attribute("name") == "description":
                    description = meta.get_attribute("content")
                    break
            
            # the html content for tokenisation
            content = driver.page_source
            return title, description,urls,content
        except Exception as e:
            raise e
        finally:
            Driver.close_driver(driver)