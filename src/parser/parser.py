import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup

from src.parser.driver import Driver
from src.constants import URL_REGEX
from src.utils.tokenizer import tokenizer

MAX_THREADS = 10 # the maximum amount of threads we need to handle the parsing
MAX_QUEUE_SIZE = 10000


class Parser:
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
    def uri_validator(self, x):
        try:
            result = urlparse(x)
            return all([result.scheme, result.netloc])
        except:
            return False

    def parse(self,url):
        '''
        This function will parse the website and go through all the links and it's content and give us the following
            1. urls
            2. title
            3. description
            4. tags
        Args:
            url (string): url that is to be parsed
        Returns:
            
            dict|None containing data about the url in format given above

        '''
        if not self.uri_validator(url):
            raise ValueError("Invalid url")
        result = dict()
        try:
            result['title'], result['description'],result['urls'],content = Driver.get_website_data(url)
            result['tags'] = self.get_tags(content)
            return result
        except ValueError as ve:
            print(ve)
            return None
        except TypeError as te:
            print(te)
            return None
        except Exception as e:
            print(e)
            return None
    
    def get_tags(self, content):
        '''
        Args:
            content (str): the HTML content
        Returns:
            List[str] list of tags
        '''
        bs = BeautifulSoup(content, 'html.parser')
        body = bs.find('body')
        content = ''.join([x for x in body.strings]).replace('\n','')
        bs.clear()
        return self.tokenize_content(content)

    def tokenize_content(self, content:str):
        '''
        Remove the prepositions and non-alphanumeric characters from the content and break them into tags
        '''
        token = tokenizer(content)
        for tk in token:
            if not re.search(r'(\w)', tk):
                token.remove(tk)
        
        return list(token)
