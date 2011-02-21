import sqlite3 as sqlite
import os
import os.path
from ci.app.delicious import Application

class DBMS(object):
    def __init__(self):
        self.app = Application()
        pass

    def make(self):
        fp = open('delicious.ddl', 'r')
        dml = fp.read()
        print dml
        self.connection.executescript(dml)

    def create(self, db_name):
        path = os.path.join(self.app.dir['data'], db_name + '.sqlite3')
        if not os.path.exists(path):
            fp = open(path, 'wb')
            fp.close()
            self.connection = sqlite.Connection(path)
            self.make()
        else:
            self.connection = sqlite.Connection(path)

    def rec_frmt(self, cur):
        record = dict()
        keys = cur.description
        data = cur.fetchone()
        index = 0
        for key in keys:
            record.update({key[0]:data[index]})
            index += 1
        return record
        
            


    def remove(self, db_name):
        pass

    def get_user(self, name):
        sql = """SELECT * FROM users WHERE name = '%(name)s'"""%{'name':name}
        cur = self.connection.execute(sql)
        return self.rec_frmt(cur) 

    def exists_user(self, name):
        sql = """SELECT COUNT(*) FROM users WHERE name = '%(name)s'"""%{'name':name}
        return self.connection.execute(sql).fetchone()     

    def add_user(self, name):
        dml = """INSERT INTO users(name) VALUES(%(name)s"""%{'name':name}
        if not self.exists_user(name):
            self.connection.execute(dml)
            self.connection.commit()
        return self.get_user(name)

    def get_url(self, url):
        sql = """SELECT * FROM urls WHERE url = '%(url)s'"""%{'url':url}
        cur = self.connection.execute(sql)
        return self.rec_frmt(cur) 

    def exists_url(self, url):
        sql = """SELECT COUNT(*) FROM urls WHERE nurl = '%(url)s'"""%{'url':url}
        return self.connection.execute(sql).fetchone()     

    def add_url(self, url):
        dml = """INSERT INTO urls(url) VALUES(%(url)s"""%{'url':url}
        if not self.exists_url(url):
            self.connection.execute(dml)
            self.connection.commit()
        return self.get_user(url)

    def get_tag(self, tag):
        sql = """SELECT * FROM tags WHERE tag = '%(tag)s'"""%{'tag':tag}
        cur = self.connection.execute(sql)
        return self.rec_frmt(cur) 

    def exists_tag(self, tag):
        sql = """SELECT COUNT(*) FROM tags WHERE tag = '%(tag)s'"""%{'tag':tag}
        return self.connection.execute(sql).fetchone()     

    def add_tags(self, tags):
        tags = tags.lower().split()
        tag_records = list()
        dml = """INSERT INTO tags(tag) VALUES (%(tag)s)"""%{'tag':tag}
        for tag in tags:
            if self.not_exists_tag(tag):
                self.connection.execute(dml)
                self.connection.commit()
            tag_records = tag_records + [self.get_tag(tag)]
        return tag_records

    def exists_user_url_tag(self, record):
        sql = """SELECT * FROM user_url_tag WHERE user_id=%(user_id) AND url_id=%(url_id)d AND tag_id=%(tag_id)d"""%record
        return self.connenction.execute(sql).fetchone()

    def add_user_url_tags(self, user_record, url_record, tags_records):
        dml = """INSERT INTO user_url_tags(user_id, url_id, tag_id) VALUES(%(user_id)d, %(url_id)d, %(tag_id)d)"""
        for tag_record in tag_records:
            tag_id = tag_record['id']
            user_id = user_record['id']
            url_id = url_record['id']
            record = {'user_id':user_id, 'url_id':url_id, 'tag_id':tag_id}
            dml_string = dml%record
            if not self.exists_user_url_tag(record):
                self.connection.execute(dml_string)
                self.connection.commit()

    def exists_description(self, record):
        sql = """SELECT COUNT(*) FROM descriptions WHERE description=%(description)s AND url_id=%(url_id)d"""%record
        return self.connection.execute(sql).fetchone()     

    def add_description(self, description, url_record):
        dml = """INSERT INTO descriptions(description, url_id) VALUES(%(description)s, %(url_id)d"""
        record = {'description':description, ' url_id':url_record['id']}
        dml_string = dml%record
        if not self.exists_description(record):
            self.connection.execute(dml_string)
            self.connection.commit()
        

    def insert(self, record):
        user_record = self.add_user(record['user'])
        url_record = self.add_url(record['url'])
        tags_records = self.add_tags(record['tags'])
        user_url_tags = self.add_user_url_tags(user_record, url_record, tags_records)

if __name__ == "__main__":
    db = DBMS()

    
