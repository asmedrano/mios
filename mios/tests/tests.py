"""
Run tests like so:
    python -m unittest discover
Make sure its from the main module directory!
SEE: http://docs.python.org/library/unittest.html#test-discovery
"""
from unittest import TestCase, main
from mios.data import *

class TestData(TestCase):

    def setUp(self):
        self.im = ImageManager('test-db')

    def test_image_save(self):
        img = Image(
            name="test image",
            description="Yadayada",
            tags = ['fun','sun']
        )

        self.im.insert([img])
        self.assertEqual(1, self.im.get_count())

    def test_image_find_one(self):
        img = Image(
            name="test image",
            description="Yadayada",
            tags = ['fun','sun']
        )
        self.im.insert([img])
        # should return an image object
        result = self.im.find_one()
        self.assertEqual(result.name, "test image")

    def test_image_find_one_query(self):
        img = Image(
            name="test image",
            description="Yadayada",
            tags = ['fun','sun']
        )

        img2 = Image(
            name="test image 2",
            description="Yadayada",
            tags = ['fun','sun']
        )
        self.im.insert([img, img2])
        # should return an image object
        result = self.im.find_one({'name':'test image 2'})
        self.assertEqual(result.name, "test image 2")

    def test_image_find(self):

        img = Image(
            name="test image",
            description="Yadayada",
            tags = ['fun','sun']
        )

        img2 = Image(
            name="test image 2",
            description="Yadayada",
            tags = ['fun','sun']
        )

        self.im.insert([img, img2])

        self.assertEqual(len(self.im.find()),2)
        self.assertEqual(len(self.im.find({'name':'test image'})), 1)

        #just making sure we get back Image objects
        r = self.im.find({'name':'test image'})
        self.assertEqual(r[0].name, 'test image')

    def test_image_update(self):

        img = Image(
            name="test image",
            description="Yadayada",
            tags = ['fun','sun']
        )

        img2 = Image(
            name="test image 2",
            description="Yadayada",
            tags = ['fun','sun']
        )

        self.im.insert([img, img2])
        self.im.update({'name':'test image'}, description="modified descrip")

        self.assertEqual(self.im.find_one().description, "modified descrip")


    def test_image_remove(self):

        img = Image(
            name="test image",
            description="Yadayada",
            tags = ['fun','sun']
        )

        img2 = Image(
            name="test image 2",
            description="Yadayada",
            tags = ['fun','sun']
        )

        self.im.insert([img, img2])

        # sanity check
        self.assertEqual(2, self.im.get_count())
        self.im.remove(img)
        self.assertEqual(1, self.im.get_count())
        # remove should always take an Image obj to keep us from destroying the
        # whole collection
        self.assertRaises(TypeError, self.im.remove , {'a':'b'})

    def tearDown(self):
        self.im.images.remove() # we always clear out the test-db
        self.im.close_conn()

if __name__ == '__main__':
    main()

