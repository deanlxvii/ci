import sqlite3 as sqlite
import os
import os.path
from ci.app.delicious import Application

dml = {'create user':"""CREATE TABLE "user_url_tags" ("id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "user_id" integer, "url_id" integer, "tag_id" integer, "created_at" datetime, "updated_at" datetime) """
       }

class DBMS(object):
    def __init__(self):
        self.app = Application()
        pass

    def create(self, db_name):
        pass

    def remove(self, db_name):
        pass

    def insert(self, record):
        pass

if __name__ == "__main__":
    db = DBMS()

    
