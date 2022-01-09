from queue import Queue
import os, threading

MAX_THREADS = 10 # the maximum amount of threads we need to handle the parsing
MAX_QUEUE_SIZE = 10000

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

def parser(url, queue:Queue):
    '''
    This function will parse the website and go through all the links and it's content and give us the following
        1. url
        2. title
        3. description
        4. tags
        5. external-links
        6. host and server (this will help to group all the pages for an website)
    one page parsed by this function i.e one html page per function call, so http://example.com will be called in one url and http://example.com/about will be called in another.
    Another thing is that we need to check if url exists or not, that's using database.
    '''
    pass