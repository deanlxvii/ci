from math import sqrt
from ci.calc.maths import *
from ci.data.critics import critics

class Recommendation(object):
	def __init__(self):
		pass

	def read(self, data):
		if type(data) == type(dict()):
				self.preferences = data

	def similarity(self, function, object1, object2):
		return function(self.preferences, object1, object2)

def intersection(preferences, collection1, collection2):
	intersect = {}
	for item in preferences[collection1]:
		if item in preferences[collection2]:
			intersect[item] = 1
	return intersect


def sim_distance(preferences,object1, object2):
	"""Returns a distance-based similarity score for object1 and object2"""
	
	shared_items = intersection(preferences, object1, object2)

	number_of_elements = len(shared_items)
	if number_of_elements == 0: 
		return 0

	values1 = [preferences[object1][item] for item in shared_items]
	values2 = [preferences[object2][item] for item in shared_items]

	return 1/(1+euclidean(values1,values2)**2)

def sim_pearson(preferences, object1, object2):
	"""Returns the Pearson correlation coefficient for object1 and object2"""

	shared_items = intersection(preferences, object1, object2)

	number_of_elements = len(shared_items)
	if number_of_elements == 0:
		return 0

	x = [preferences[object1][item] for item in shared_items]
	y = [preferences[object2][item] for item in shared_items]
	return pearson(x,y)


if __name__ == "__main__":
	print sim_distance(critics,'Lisa Rose','Gene Seymour')
	print sim_distance(critics,'Lisa Rose','Lisa Rose')

	print sim_pearson(critics, 'Lisa Rose', 'Gene Seymour')
	print '------------------------------------------------'
	recommend = Recommendation()
	recommend.read(critics)
	print recommend.similarity(sim_distance, 'Lisa Rose', 'Gene Seymour')
