from threading import Thread
from src.engine import db, queue
from src.parser.parser import Parser

class ParserHandler:
    '''
    This will maintain the queue and threads, will have a mainloop which will keep parsering.
    there will be a maximum amount of threads given to each threads and will be passed an url, threads will append resulten data to data array at their 
    designated positions. 
    A event loop will check for data from data array and will add data whenever it finds one.
    A main function will be there which will be wrapper and caller for all these.
    '''

    def __init__(self, no_of_threads=10):
        self.thread_holders = [None]*no_of_threads
        self.max_no_of_threads = no_of_threads
        self.data_holder = {}
        for i in range(self.max_no_of_threads):
            self.data_holder[i]=[]
        
        self.set_allot_id = set()
    def __create_wrapper(self):
        '''
        This function will create a function which will be handling all the parsing related stuff such as handling errors and 
        '''
        def parser_wrapper(url:str, allotId:int, dataHolder:dict):
            if allotId not in dataHolder:
                return
            parser = Parser()
            if not parser.uri_validator(url):
                dataHolder[allotId].append({
                        'error': 'Invalid url'
                })
                return
            
            try:
                data = parser.parse(url)
                dataHolder[allotId].append(data)
            except Exception as e:
                dataHolder[allotId].append({
                        'error': str(e)
                })
            
            return parser_wrapper
    
    def __check_empty_or_finished_thread(self):
        '''
        Simple job of iterating through iterating through set of thread holders and adding the allot id of allot which are either none or finished.
        '''
        for i in range(self.max_no_of_threads):
            try:
                if self.thread_holders[i] == None:
                    self.set_allot_id.add(i)
                elif not self.thread_holders[i].is_alive():
                    self.set_allot_id.add(i)
            except:
                self.set_allot_id.add(i)
    
    def __iterate_over_data_holder(self):
        '''
        Another simple job that is we have to iterate over the set and find the allot id which are free now and extract the data from the data holder 
        and do some simple validation and return an array of data. 
        '''
        data_arr = list()
        for free_alot in self.set_allot_id:
            for data in self.data_holder.get(free_alot,[]):
                if not data or data.get('error'): # None value and error values
                    print(data.get('error'))
                else:
                    data_arr.append(data)
            
            self.data_holder[free_alot] = list()

        return data_arr
    
    def ___create_parser_threads(self):
        '''
        iterates through the set of allot id and then creates threads and assign them to allot id
        '''
        wrapper = self.__create_wrapper()
        for allot_id in self.set_allot_id.copy():
            url = queue.get_url_at_front()
            if not url:
                print('Empty Queue')
                break

            th = Thread(target=wrapper, args=(url,allot_id, self.data_holder))
            th.start()
            th.setDaemon(True)
            self.thread_holders[allot_id] = th
            self.set_allot_id.remove(allot_id)

    def __data_addition_to_db_and_queue(self, data_list:list):
        '''
        This takes the list of data recieved from the parser and 
            - adds the next urls to queue,
            - adds record in db
        '''
        for data in data_list:
            try:
                for url in data.get('urls', []):
                    queue.add_url_to_queue(url)
                
                db.add_website_data(**data)
            except Exception as e:
                print(e)
    
    def runner(self):
        try:
            while True:
                self.__check_empty_or_finished_thread()
                data_list = self.__iterate_over_data_holder()
                self.__data_addition_to_db_and_queue(data_list)
                self.___create_parser_threads()
                pass
        except KeyboardInterrupt:
            print('Program exitted')
            return 0
            pass
        except Exception as e:
            print(e)
            return -1
        
                    