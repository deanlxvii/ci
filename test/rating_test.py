from ci.data.critics import critics
from ci.recommend import *
import unittest

class TestRatings(unittest.TestCase):
    def setUp(self):
        self.ratings = Ratings()
        self.ratings.format(critics)

    def test_created(self):
        self.assertTrue(self.ratings is not None)

    def test_id(self):
        self.assertEqual(len(self.ratings.id), 7)
        self.assertTrue('Toby' in self.ratings.id)

    def test_rating(self):
        rating = self.ratings['Toby']
        self.assertTrue(len(rating)>0)
        self.assertEqual(len(rating),3)

    def test_intersection(self):
        rating1 = self.ratings['Toby']
        rating2 = self.ratings['Michael Phillips']
        intersection = rating1 * rating2
        
        self.assertEqual(len(intersection),2)
        self.assertTrue('Snakes on a Plane' in intersection.keys())


if __name__ == "__main__":
    unittest.main()
