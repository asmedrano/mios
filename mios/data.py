import simplejson as json
from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime

class Image(object):
    """ a simple image model """
    def __init__(self, name=None, description=None, published=False, tags=[]):
        self.id = None
        self.name = name
        self.description = description
        self.created_at = None # auto generated when saved
        self.tags = tags # tags....
        self.published = published # is this picture published?
        self.versions = [] # list of resized versions of this image

    def to_dict(self):
        self.created_at = datetime.datetime.today()
        d = {
            'name' : self.name,
            'description' : self.description,
            'created_at': self.created_at,
            'tags' : self.tags,
            'published':self.published,
            'version':self.versions
        }

        if self.id:
            d['_id'] = ObjectId(self.id)

        return d


class ImageManager(object):
    """ Manages the CRUD for images on disk and in mongodb"""
    def __init__(self, dbname):
        self.connection = MongoClient('127.0.0.1', 27017)
        self.db = self.connection[dbname]
        self.images = self.db.images

    def _image_from_bson(self, bson):
        """ Return an Image from a bson result"""
        print bson

    def insert(self, image_objs):
        """ Insert one or many image objects. Image objs should be a list of image objects, ex: [img1, img2]"""
        self.images.insert([img.to_dict() for img in image_objs])

    def find_one(self, query=None):
        """ Get one Image by query. Returns Image object
            query should be a pymongo query Dict thing {}
        """
        if query:
            return self.images.find_one(query)
        else:
            return self.images.find_one()

    def find(self, query=None):
        """ get more than a single document as the result of a query. Return Cursor instance"""
        if query:
            return self.images.find(query)
        else:
            return self.images.find()

    def get_count(self):
        return self.images.count()

    def close_conn(self):
        self.connection.close()


