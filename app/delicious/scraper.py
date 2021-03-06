import cPickle
import time
from pydelicious import get_popular, get_userposts, get_urlposts, get_tagposts
import sys, os, os.path
from ci.app.delicious.application import Application

class Scraper(object):
    """
    Scrape data from del.ico.us
    Depends on pydelicious!
    """
    def __init__(self, verbose=False):
        self.app = Application()
        self.object_dict = dict()
        self.verbose = verbose

    @property
    def data(self):
        return self.object_dict

    def load(self, tag):
        """
        Given the tag it load the dict form a file
        delicious_[tag].dat
        """
        filename = 'delicious_' + tag + '.dat'
        filename = os.path.join(self.app.dir['data'], filename)
        self.object_dict = cPickle.load(open(filename, 'r'))
        return self.object_dict


    def save(self, tag):
        """
        Saves the scraped data in a .dat file with
        a prefix delicious_ follow by the tag
        """
        filename ='delicious_'+ tag + '.dat'
        filename = os.path.join(self.app.dir['data'], filename)
        cPickle.dump(self.object_dict, open(filename, 'w'))


class TagItemScraper(Scraper):
    def __init__(self):
        Scraper.__init__(self)

    def scrape(self, tag, custom_object_names=None):
        pass

    def select_from_popular(self, tag, count=5):
        for popular in get_popular(tag=tag)[0:count]:
            for post in get_urlposts(popular['url']):
                tags = post['tags'].lower().split()
                for object in tags:
                    self.object_dict[object] = dict()

    def initialize_object_dict(self, tag, count=5):
        if type(tag) == type(str()):
            self.select_from_popular(tag)

        if type(tag) == type(list()):
            for a_tag in tag:
                self.select_from_popular(a_tag)

    def fill_items(self):
        all_items = dict()
        for object in self.object_dict:
            for i in range(3):
                try:
                    posts = get_tagposts(object)
                    break
                except:
                    print "Failed tag "+object+", retrying"
                    time.sleep(4)
            for post in posts:
                url = post['url']
                self.object_dict[object][url]=post['tags'].lower().split()



class UserItemScraper(Scraper):
    def __init__(self):
        Scraper.__init__(self)

    def scrape(self,tag, custom_object_names=None):
        """
        scrape the popular posts of a tag,
        optional: include one (string) or more objects (list)
        with custom_object_names
        """
        self.initialize_object_dict(tag)
        if custom_object_names:
            self.add(custom_object_names)
        self.fill_items()
        self.save(tag)
        return self.object_dict
    
    def add(self, object_names):
        """
        Add some other names to the initial dict
        """
        if type(object_names) == type(str()):
            self.object_dict[object_names] = dict()
        if type(object_names) == type(list()):
            for object_name in object_names:
                self.object_dict[object_name] = dict()

    
    def initialize_object_dict(self, tag, count=5):
        """
        Initialize object (user) dict with users from
        the popular posts for tag
        """
        for popular in get_popular(tag=tag)[0:count]:
            for posts in get_urlposts(popular['url']):
                object = posts['user']
                if self.verbose: print object
                self.object_dict[object] = dict()

    def fill_items(self):
        all_items = dict()
        for object in self.object_dict:
            for i in range(3):
                try:
                    posts = get_userposts(object)
                    break
                except:
                    print "Failed user "+object+", retrying"
                    time.sleep(4)
            for post in posts:
                if self.verbose: print post
                url = post['url']
                self.object_dict[object][url]=1.0
                all_items[url]=1

        for ratings in self.object_dict.values():
            for item in all_items:
                if self.verbose: print item
                if item not in ratings:
                    ratings[item] = 0.0


