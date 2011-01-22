from ci.calc.maths import *
from ci.data.critics import critics
from ci.ratings import *
from ci.recommendations import Recommendation
import unittest

class TestRecommendation(unittest.TestCase):
	def setUp(self):
		self.recommend = Recommendation(critics)

	def test_pearson_same(self):
		self.assertEqual(self.recommend.similarity(pearson, 'Lisa Rose', 'Lisa Rose'),1)

	def test_pearson(self):
		self.assertEqual(round(self.recommend.similarity(pearson, 'Lisa Rose', 'Gene Seymour'),8),round(0.396059017191,8))

	def test_euclidean_same(self):
		self.assertEqual(self.recommend.similarity(euclidean, 'Lisa Rose', 'Lisa Rose'),1)
	
	def test_euclidean(self):
		self.assertEqual(round(self.recommend.similarity(euclidean, 'Lisa Rose', 'Gene Seymour'),8),round(0.148148148148,8))

	def test_type(self):
		self.assertEqual(type(self.recommend.preferences),type(Ratings()))

	def test_get_rating(self):
		rating = self.recommend.ratings['Toby']
		self.assertEqual(type(rating), type(Rating()))

	def test_intersection(self):
		rating1 = self.recommend.ratings['Toby']
		rating2 = self.recommend.ratings['Michael Phillips']
		intersection = rating1 * rating2
		self.assertEqual(len(intersection),2)

	def test_top_matches(self):
		self.assertEqual(len(self.recommend.top_matches('Toby',pearson, n=3)), 3)

	def test_get_recommendations(self):
		recommendations = self.recommend.get_recommendations('Toby', pearson)
		self.assertEqual(len(recommendations)>0, True)

if __name__ == "__main__":
	unittest.main()
