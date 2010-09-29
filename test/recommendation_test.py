from ci.calc.maths import *
from ci.data.critics import critics
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
if __name__ == "__main__":
	unittest.main()
