'''
This will hold all the functions which are related to search and storing In database.
'''
import sqlite3
import os, time

from src.utils.env import cwd_path
from src.constants import (CHECK_IF_URL_EXISTS, CREATE_QUEUE_TABLE_QUERIES, CREATE_SEARCH_TABLE_QUERIES, 
ADD_TO_SEARCH_TABLE, GET_ALL_UNPARSED_URLS, MARK_URL_COMPLETED_STATUS, ADD_TO_QUEUE_TABLE)

class DatabaseHandler:

    def __init__(self, path=None):
        if not path:
            path = os.path.join(cwd_path(), 'test.db')
        
        if not os.path.exists(path):
            with open(path, 'x') as _:
                pass
        
        self.path = path

        self.__create_base_tables()
    
    def __create_connection(self):
        conn = None
        conn = sqlite3.connect(self.path)
        return conn

    def __create_base_tables(self):
        '''
        Will create the basic tables which we will require for these application.
        '''

        conn = None
        try:
            conn = self.__create_connection()
            cursor = conn.cursor()
            cursor.execute(CREATE_SEARCH_TABLE_QUERIES)
            time.sleep(0.5)

            cursor.execute(CREATE_QUEUE_TABLE_QUERIES)
        except Exception as e:
            print(e)
            return
        finally:
            if conn:
                conn.close()
        
    def add_website_data(self, **data):
        '''
        as the name suggest it will add the data from the parser to the database
        '''
        conn = None

        url = data.get('url')
        title = data.get('title')
        description = data.get('description', 'NULL')
        tags = " ".join(data.get('tags', []))
        data = (url, title, description, tags)

        try:
            conn = self.__create_connection()
            cursor = conn.cursor()
            cursor.execute(ADD_TO_SEARCH_TABLE, data)
            conn.commit()

            time.sleep(0.1)

            self.mark_url_as_done_in_queue(conn, url)
        except Exception as e:
            print(f"{e} \n Gotcalled in add_website_data")
            raise e
        finally:
            if conn:
                conn.close()

    def mark_url_as_done_in_queue(self,conn, url, close = False):
        '''
        This is the function we will call whenever we need to mark a url as completed.
        '''
        
        
        try:
            if not conn:
                conn = self.__create_connection()
            conn.cursor().execute(MARK_URL_COMPLETED_STATUS, (url,))
            conn.commit()
        except Exception as e:
            print(f"{e} \n Gotcalled in mark_url_as_in_queue")
            raise e
        finally:
            if conn and close:
                conn.close()

    def add_url_to_queue(self, url:str):
        '''
        This function will just add the url to queue table in the db
        '''
        conn = None
        try:
            conn = self.__create_connection()
            conn.cursor().execute(ADD_TO_QUEUE_TABLE, (url.trim(),))
            conn.commit()
            return True
        except Exception as e:
            print(f"{e} \n Gotcalled in add_url_to_queue")
            raise e
        finally:
            if conn:
                conn.close()
    

    def check_if_url_is_present(self, url):
        '''
        Args:
            url(str) url to be searched
        Returns:
            bool : True if exists and False if not
        '''

        conn = None

        try:
            conn = self.__create_connection()
            cur = conn.execute(CHECK_IF_URL_EXISTS, (url,))
            row = cur.fetchone()
            return len(row) >0 and row[1] == url
        except Exception as e:
            print(f"{e} \n Gotcalled in check_if_url_is_present")
            raise e
        finally:
            if conn:
                conn.close()
    
    def get_all_unparsed_url(self):
        '''
        Get all the unparsed data.
        returns:
            List[str] : list containing the urls
        '''
        conn = None

        try:
            conn = self.__create_connection()
            cur = conn.cursor()
            cur.execute(GET_ALL_UNPARSED_URLS)
            rows = cur.fetchall()
            res = []
            for row in rows:
                res.append(row[0])
            return res
        except Exception as e:
            print(f"{e} \n Gotcalled in get_all_unparsed_url")
            raise e
        finally:
            if conn:
                conn.close()


        

