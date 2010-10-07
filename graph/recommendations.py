from ci.data.critics import critics
from pylab import *
from ci.recommendations import Recommendation as RecommendationData

class Recommendation(RecommendationData):
	def __init__(self, data):
		RecommendationData.__init__(self, data)

	def first_score(self):
		id = self.ratings.keys()[0]
		item = self.ratings[id].keys()[0]
		return self.ratings[id][item]

	@property
	def min_score(self):
		min = self.first_score()
		for id in self.ratings:
			for item in self.ratings[id]:
				if self.ratings[id][item] < min:
					min = self.ratings[id][item]
		return min

	@property
	def max_score(self):
		max = self.first_score()
		for id in self.ratings:
			for item in self.ratings[id]:
				if self.ratings[id][item] > max:
					min = self.ratings[id][item]
		return min

	def draw(self, item1, item2):
		p1 = []
		p2 = []
		ob = []
		for object in self.ratings:
			try:
				items = self.ratings[object].keys()
				select1 = [item for item in items if item1 in item][0]
				select2 = [item for item in items if item2 in item][0]
				p1 = p1 + [self.ratings[object][select1]]
				p2 = p2 + [self.ratings[object][select2]]
				ob = ob + [object]
			except:
				pass
		axis([0 ,self.max_score + 1, 0, self.max_score + 1])
		xlabel(item1)
		ylabel(item2)
		plot(p1,p2,'ro')
		show()


if __name__ == '__main__':
	g = Recommendation(critics)
	print g.preferences
	print g.min_score, g.max_score
	g.draw('Dupree','Snakes')
