from ci.calc.maths import *
from ci.data.critics import critics
from ci.recommend import *
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
		matches = self.recommend.top_matches('Toby', pearson, n=3)
		self.assertEqual(len(matches), 3)
		self.assertEqual(matches[0], (0.99124070716192991,'Lisa Rose'))
		self.assertEqual(matches[1], (0.92447345164190486,'Mick LaSalle'))
		self.assertEqual(matches[2], (0.89340514744156474,'Claudia Puig'))

	def test_get_recommendations(self):
		recommendations = self.recommend.get_recommendations('Toby', pearson)
		self.assertEqual(len(recommendations), 3)
		self.assertEqual(recommendations[0],(3.3477895267131013,'The Night Listener'))
		self.assertEqual(recommendations[1],(2.8325499182641618,'Lady in the Water'))
		self.assertEqual(recommendations[2],(2.5309807037655645,'Just My Luck'))
		
		recommendations = self.recommend.get_recommendations('Toby', euclidean)
		self.assertEqual(len(recommendations), 3)
		self.assertEqual(recommendations[0],(3.5002478401415877,'The Night Listener'))
		self.assertEqual(recommendations[1],(2.7561242939959363,'Lady in the Water'))
		self.assertEqual(recommendations[2],(2.461988486074373,'Just My Luck'))

	def test_reverse(self):
		reversed = self.recommend.reverse()
		recommendations = Recommendation(reversed)
		matches = recommendations.top_matches('Superman Returns', pearson)
		self.assertEqual(len(matches),5)
		self.assertEqual(matches[0], (0.65795169495976946, 'You, Me and Dupree'))
		self.assertEqual(matches[1], (0.48795003647426888,'Lady in the Water'))
		self.assertEqual(matches[2], (0.11180339887498941,'Snakes on a Plane'))
		self.assertEqual(matches[3], (-0.17984719479905439,'The Night Listener'))
		self.assertEqual(matches[4], (-0.42289003161103106,'Just My Luck'))

	def test_get_recommended_items(self):
		similar_items = self.recommend.calculate_similar_items()
		recommendations = self.recommend.get_recommended_items(similar_items, 'Toby')
		self.assertEqual(recommendations[0], (3.182634730538922, 'The Night Listener'))
		self.assertEqual(recommendations[1],(2.5983318700614575, 'Just My Luck'))
		self.assertEqual(recommendations[2],(2.4730878186968841, 'Lady in the Water'))


if __name__ == "__main__":
	unittest.main()
