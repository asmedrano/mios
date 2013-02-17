"""
Run tests like so:
    python -m unittest discover
Make sure its from the main module directory!
SEE: http://docs.python.org/library/unittest.html#test-discovery
"""
from unittest import TestCase, main

class TestSimple(TestCase):

    def setUp(self):
        pass

    def test_sample(self):
        self.assertEqual(1+1, 2)

    def tearDown(self):
        pass

if __name__ == '__main__':
    main()

