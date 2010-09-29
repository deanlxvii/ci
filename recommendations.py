from math import sqrt
from ci.calc.maths import *

class Recommendation(object):
	"""
	Make recommendation based on een system with objects, items and weights.
	Every object has some items and every item has a weight
	"""
	def __init__(self, data):
		self.format(data)

	def format(self, data):
		"""
		Format data
		"""
		if type(data) == type(dict()):
				self.preferences = data

	def intersection(self, collection1, collection2):
		_intersection = {}
		for item in self.preferences[collection1]:
			if item in self.preferences[collection2]:
				_intersection[item] = 1
		return _intersection

	def empty(self,intersection):
		if len(intersection) == 0:
			return True
		return False

	def euclidean_correction(self, value):
		return 1/(1+value**2)

	def similarity(self, function, object1, object2):
		shared_items = self.intersection(object1, object2)
		if self.empty(shared_items):
			return 0
		weights1 = [self.preferences[object1][item] for item in shared_items]
		weights2 = [self.preferences[object2][item] for item in shared_items]
		if function.__name__ == 'euclidean':
			return self.euclidean_correction(function(weights1, weights2))
		return function(weights1, weights2)
