import simplejson as json
from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime
import os

class Image(object):
    """ a simple image model """
    def __init__(self, _id=None, name=None, description=None, published=False, tags=[], versions=[]):
        self._id = _id
        self.name = name
        self.description = description
        self._tags = tags # tags....
        self.published = published # is this picture published?
        self.versions = versions # list of resized versions of this image

    @property
    def id(self):
        if self._id:
            return ObjectId(self._id)
        else:
            return None
    @property
    def tags(self):
        return ', '.join(self._tags)

    def to_dict(self):
        self.created_at = datetime.datetime.today()
        d = {
            'name' : self.name,
            'description' : self.description,
            'tags' : self._tags,
            'published':self.published,
            'versions':self.versions,
        }

        if self._id:
            d['_id'] = self.id

        return d

    def get_file_name(self):
        fname, ftype = self.name.rsplit(".")
        return fname + "_" + str(self._id) + "."+ftype

    def get_file_path(self):
        return os.path.join(os.path.dirname(__file__), 'media', self.get_file_name())


class ImageManager(object):
    """ Manages the CRUD for images on disk and in mongodb"""
    def __init__(self, dbname):
        self.connection = MongoClient('127.0.0.1', 27017)
        self.db = self.connection[dbname]
        self.images = self.db.images

    def insert(self, image_objs):
        """ Insert one or many image objects. Image objs should be a list of image objects, ex: [img1, img2]"""
        return self.images.insert([img.to_dict() for img in image_objs])

    def find_one(self, query=None):
        """ Get one Image by query. Returns Image object
            query should be a pymongo query Dict thing {}
        """
        if query:
            q_results = self.images.find_one(query)
        else:
            q_results = self.images.find_one()

        if q_results:
            return Image(**q_results)
        else:
            return None

    def find(self, query=None):
        """ get more than a single document as the result of a query. Return Cursor instance"""
        results = None
        if query:
            q_results = self.images.find(query)
        else:
            q_results = self.images.find()

        if q_results:
            results = []
            for result in q_results:
                results.append(Image(**result))
        return results

    def update(self, query, **kwargs):
        """ Update an existing Image, finding it by its id
            query should be a valid pymongo spec
            **kwargs are any properties in an Image
        """
        return self.images.update(query, {"$set":kwargs})

    def remove(self, img_obj):
        """ Remove One Item from the collection """
        if img_obj:
            if isinstance(img_obj, Image):
                self.images.remove(img_obj.to_dict())
                return True
            else:
                raise TypeError('img_obj should be instance of Image')
        else:
            return False

    def get_count(self):
        return self.images.count()

    def get_tags(self):
        return self.images.distinct('tags')

    def close_conn(self):
        self.connection.close()


