import os
import pathlib
import sqlite3
from sqlite3 import Error
from log4python.Log4python import log as Logger

class DBService:
    def __init__(self) -> None:
        self.log = Logger("main")
        #set up the paths
        self.dbdir = os.path.join(os.getcwd(), 'db')
        self.dbpath = os.path.join(self.dbdir, "pythonsqlite.db")

        #self.log.info(self.dbdir)
        #self.log.info(self.dbpath)

        #make sure the folder exists
        path = pathlib.Path(self.dbdir)
        path.mkdir(parents=True, exist_ok=True)
        #create the db
        self.create_connection(self.dbpath)


    def create_connection(self, db_file):
        """ create a database connection to a SQLite database """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            self.log.info(f"connected to sqlite3.version:{sqlite3.version}, path:{db_file}")
        except Error as e:
            self.log.error(e)
        finally:
            if conn:
                conn.close()


