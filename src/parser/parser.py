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
    In this class we are validating url and then parsing the url using webdriver and retriveing the, tags, description title, and other links
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
            result['url'] = url
            return result
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
        for tk in token.copy():
            if not re.search(r'(\w)', tk):
                token.remove(tk)
        
        return list(token)
