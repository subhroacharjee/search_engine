from src.engine import db, queue

class ParserHandler:
    '''
    This will maintain the queue and threads, will have a mainloop which will keep parsering.
    there will be a maximum amount of threads given to each threads and will be passed an url, threads will append resulten data to data array at their 
    designated positions. 
    A event loop will check for data from data array and will add data whenever it finds one.
    A main function will be there which will be wrapper and caller for all these.
    '''