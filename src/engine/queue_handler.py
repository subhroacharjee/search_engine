from src.engine import db

class QueueHandler:
    '''
    - it is going to fetch the urls which are in the database that are not parsed and add it to program queue
    - in case a new element is added it will be added in db as well
    - also will have a static queue
    '''

    def __init__(self):
        try:
            unparsed_url = db.get_all_unparsed_url()
        except Exception as e:
            print(e)
            raise ValueError('Queue can\'t be initated due to db failure.')
        self.__queue = []

        for urls in unparsed_url:
            self.__queue.insert(0, urls)
        
    def add_url_to_queue(self, url):
        try:
            db.add_url_to_queue(url)
        except Exception as e:
            print(e)
            raise ValueError('Url addition was interupted by db failure.')
        
        self.__queue.insert(0, url)
    
    def get_url_at_front(self):
        try:
            url = self.__queue.pop()
            while not db.check_if_url_is_parsed(url):
                url = self.__queue.pop()
            
            return url
        except IndexError:
            return None
        except Exception as e:
            print(e)
            raise ValueError('Can\'t get data from queue due to db error.')