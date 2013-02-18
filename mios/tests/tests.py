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

    def tearDown(self):
        self.im.images.remove() # we always clear out the test-db
        self.im.close_conn()

if __name__ == '__main__':
    main()

