'''
what do i want to do?
so we already have a parser which takes a url and returns us a dict which contains the data for that url. Now what i want is to
- create function/class to call the parser and store the details onto a database
    - we need a database storage device which will store the data coming from the parser to the database
    - we need a function to access the database and then perform curd operation.
- create a QUEUE which will take the urls from the data provided from the data and then call the parser again.
- we needa queue operation class for this
- also we need threads to do the threading on parser and no of threads will be either come from env or something
    - so threading, we will use parser function as target function will store there the input to some array.
    - we need a component to constantly check if the array is filled with some data or not
    - we need to check if any of the threads has finished or not. so in case they have finished we will we be performing a series of operations.
        - first take the data from the array and then store it in db and the queue.
        - will take the first component of the queue in and create a new wrapper function which will incase call parser


1. Create a wrapper class which will call n parser function in parallel and store there data on a array
2. the wrapper class will have an infinite loop which will constantly check on the threads and check which one has finished.
3. In case a thread finishes it will take the data available in the array and then store it to database using database model.
4. we need that wrapper class to have a queue which can hold the urls and fire off parser function using url inside the queue.
'''
from .database_handler import DatabaseHandler
from .queue_handler import QueueHandler
import os

DB_PATH = os.environ.get('DB_PATH')

db = DatabaseHandler(DB_PATH)
queue = QueueHandler()