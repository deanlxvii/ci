import sqlite3 as sqlite
import os
import time, datetime
import os.path
from ci.app.delicious import Application

import pydelicious as d

class DBMS(object):
    """
    DBMS for the delicious app
    """
    def __init__(self):
        self.app = Application()
        pass

    def make(self):
        """
        DDL Create the tables
        """
        fp = open('delicious.ddl', 'r')
        dml = fp.read()
        print dml
        self.connection.executescript(dml)

    def get_path(self, db_name):
        return os.path.join(self.app.dir['data'], db_name + '.sqlite3')

    def connect(self, db_name):
        path = self.get_path(db_name)
        self.connection = sqlite.Connection(path)
    def create(self, db_name):
        """
        Create a delicious sqlite db (file) with name db_name.
        The file will be written in user dir (~) .ci/delicious/dat
        """
        path = self.get_path(db_name)
        if not os.path.exists(path):
            fp = open(path, 'wb')
            fp.close()
            self.connect(db_name)
            self.make()
        else:
            self.connect(db_name)


    def rec_frmt(self, cur):
        """
        format the data in a dict {'attribute_name':value}
        """
        record = dict()
        keys = cur.description
        data = cur.fetchone()
        print data
        index = 0
        for key in keys:
            record.update({key[0]:data[index]})
            index += 1
        return record
        
    def remove(self, db_name):
        """
        Delete sqlite db with name db_name
        """
        path = self.get_path(db_name)
        os.remove(path)

    def insert(self, record):
        print '<record> : ',record
        self.timestamp = datetime.datetime.now()
        user_record = self.add_user(record['user'])
        url_record = self.add_url(record['url'])
        tags_records = self.add_tags(record['tags'])
        self.add_description(record['description'], url_record)
        self.add_user_url_tags(user_record, url_record, tags_records)
        self.add_url_date(record['dt'], url_record, user_record)
        
    def exists(self, sql, data=None):
        print '<exists> : ', sql
        if not data:
            return self.connection.execute(sql).fetchone()[0] > 0
        return self.connection.execute(sql, data).fetchone()[0] > 0
        

    def execute(self, a_string, data=None, commit=False):
        print '<execute> : ', a_string
        if data:
            cursor = self.connection.execute(a_string, data)
        else:
            cursor = self.connection.execute(a_string)
        if commit:
            self.connection.commit()
        return cursor
        
    # USER

    def get_user(self, name):
        sql = """SELECT * FROM users WHERE name = '%(name)s'"""%{'name':name}
        cur = self.execute(sql)
        return self.rec_frmt(cur) 

    def exists_user(self, name):
        sql = """SELECT COUNT(*) FROM users WHERE name = '%(name)s'"""%{'name':name}
        return self.exists(sql) 

    def add_user(self, name):
        dml = """INSERT INTO users(name, created_at, updated_at) VALUES( ?, ?, ?)"""
        if not self.exists_user(name):
            self.execute(dml, data=(name,self.timestamp,self.timestamp), commit=True)
        return self.get_user(name)

    # URL

    def get_url(self, url):
        sql = """SELECT * FROM urls WHERE url = '%(url)s'"""%{'url':url}
        cur = self.execute(sql)
        return self.rec_frmt(cur) 

    def exists_url(self, url):
        sql = """SELECT COUNT(*) FROM urls WHERE url = '%(url)s'"""%{'url':url}
        return self.exists(sql)     

    def add_url(self, url):
        dml = """INSERT INTO urls(url, created_at, updated_at) VALUES( ?, ?, ?)"""
        if not self.exists_url(url):
            self.execute(dml, data=(url,self.timestamp,self.timestamp), commit=True)
        return self.get_url(url)

    # TAG

    def get_tag(self, tag):
        sql = """SELECT * FROM tags WHERE tag = '%(tag)s'"""%{'tag':tag}
        cur = self.execute(sql)
        return self.rec_frmt(cur) 

    def exists_tag(self, tag):
        sql = """SELECT COUNT(*) FROM tags WHERE tag = '%(tag)s'"""%{'tag':tag}
        return self.exists(sql)     

    def add_tags(self, tags):
        tags = tags.lower().split()
        tag_records = list()
        dml = """INSERT INTO tags(tag, created_at, updated_at) VALUES (?, ?, ?)"""
        for tag in tags:
            if tag[-1] == ',':
                tag = tag[0:-1]
            if not self.exists_tag(tag):
                self.execute(dml, data=(tag,self.timestamp, self.timestamp), commit=True)
            tag_records = tag_records + [self.get_tag(tag)]
        return tag_records


    # DESCRIPTION

    def exists_description(self, record):
        #sql = """SELECT COUNT(*) FROM descriptions WHERE description="%(description)s" AND url_id=%(url_id)d"""%record
        sql = """SELECT COUNT(*) FROM descriptions WHERE description=? AND url_id=?"""
        return self.exists(sql,record)     

    def add_description(self, description, url_record):
        dml = """INSERT INTO descriptions(description, url_id, created_at, updated_at) VALUES(?, ?, ?, ?)"""
        if not self.exists_description((description, url_record['id'])):
            record = (description, url_record['id'], self.timestamp, self.timestamp)
            self.execute(dml, data=record, commit=True)

    # EXTENDED

    def exists_extended(self, record):
        sql = """SELECT COUNT(*) FROM extendeds WHERE extended=%(extended)s AND url_id=%(url_id)d"""%record
        return self.exists(sql)

    def add_extended(self, extended, url_record, user_record):
        dml = """INSERT INTO extendeds(extended, url_id, user_id) VALUES(%(extended)s, %(url_id)d, %(user_id)d)"""
        record = {'extended':extended,'url_id':url_record['id'], 'user_id':user_record['id']}
        dml_string = dml%record
        if not self.exists_extended(record):
            self.execute(dml_string, commit=True)

    # USER URL TAG

    def exists_user_url_tag(self, record):
        sql = """SELECT COUNT(*) FROM user_url_tags WHERE user_id=%(user_id)d AND url_id=%(url_id)d AND tag_id=%(tag_id)d"""%record
        return self.exists(sql)

    def add_user_url_tags(self, user_record, url_record, tag_records):
        dml = """INSERT INTO user_url_tags(user_id, url_id, tag_id, created_at, updated_At) VALUES(?, ?, ?, ?, ?)"""
        for tag_record in tag_records:
            tag_id = tag_record['id']
            user_id = user_record['id']
            url_id = url_record['id']
            record = (user_id, url_id, tag_id, self.timestamp, self.timestamp)
            if not self.exists_user_url_tag({'user_id':user_id,'url_id':url_id,'tag_id':tag_id}):
                self.execute(dml, data=record, commit=True)

    # URL DATE

    def to_datetime(self, time_string):
        datetime_format = '%Y-%m-%dT%H:%M:%SZ'
        t = time.strptime(time_string, datetime_format)
        return datetime.datetime(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)

    def exists_url_date(self, record):
        sql = """SELECT COUNT(*) FROM url_dates WHERE url_date=? AND url_id=? AND user_id=?"""
        return self.exists(sql, record)

    def add_url_date(self, dt, url_record, user_record):
        dml = """INSERT INTO url_dates(url_date, url_id, user_id, created_at, updated_at) VALUES(?, ?, ?, ?, ?)"""
        if not self.exists_url_date((self.to_datetime(dt),url_record['id'],user_record['id'])):
            record = (self.to_datetime(dt), url_record['id'], user_record['id'], self.timestamp, self.timestamp)
            self.execute(dml, data=record, commit=True)


if __name__ == "__main__":
    db = DBMS()
    users = []
    popular = d.get_popular()
    db.create('delicious')
    for pop in popular:
        db.insert(pop)
        if pop['user'] not in users:
            users += [pop['user']]

    for user in users:
        up = d.get_userposts(user)
        for post in up:
            db.insert(post)

# Error in exists description
#{'extended': '', 'description': u'Want to know "What is insomina?"', 'tags': u'insomina health questions', 'url': u'http://www.healthysparx.com/questions/2570/what-exactly-is-insomnia/?cid=5rcf01', 'user': u'great.pinku', 'dt': u'2011-02-16T19:01:55Z'}
