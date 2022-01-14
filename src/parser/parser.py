import os, re
from bs4 import BeautifulSoup as bs
from selenium import webdriver

from src.utils.env import cwd_path
from src.constants import URL_REGEX

URL_PATTERN = re.compile(URL_REGEX)


MAX_THREADS = 10 # the maximum amount of threads we need to handle the parsing
MAX_QUEUE_SIZE = 10000


options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome(os.path.join(cwd_path(),'chromedriver'), chrome_options=options)

'''
So what we want?
we want to parse a website and store external links to other website to the queue
we want that there will be a thread which will call parser to a website.
we want a program to check the queue and create thread with one thread parsing 1 website if entry exists in queue
we want a program which will check if queue if full or not, if queue is full then it will make that thread wait, until all the urls are in the queue
we want a program to check if we are using maximum amount of threads and in case we are doing that we will add no more threads until a thread is stopped.
we want each thread to parse the data of websites and data to db[name of website, title, description]
also we want to run all of these as well
also we want to save the queue data to some json file so that when process restarts after a crash or restarting it doesn't starts from the begining.
we need a good exception and signal handling functions
'''

def parser(url):
    '''
    This function will parse the website and go through all the links and it's content and give us the following
        1. urls
        2. title
        3. description
        4. tags
    Args:
        url (string): url that is to be parsed
    Returns:
        int|None the error code in case of error
        dict|None containing data about the url in format given above

    '''

    try:
        title, description,urls,content = run_selenium(url)
        return None, content
    except ValueError as ve:
        return -1, None
    except Exception as e:
        print(e)
        return -10, None
    pass

def run_selenium(url):
    if not re.search(URL_PATTERN, url):
        raise ValueError("Invalid url")
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


   