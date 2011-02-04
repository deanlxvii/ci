from ci.data.critics import critics
from pylab import *
from ci.recommend import Recommendation as RecommendationData

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
					max = self.ratings[id][item]
		return max


	def graph_config(self, item1, item2 , x, y, plottype):
		axis([0 ,self.max_score + 1, 0, self.max_score + 1])
		xlabel(item1)
		ylabel(item2)
		plot(x,y,plottype)

	def plot_text(self, x, y, txt):
		double = []
		step = -0.2
		for i in range(0, len(txt)):
			if (x[i],y[i]) in double:
				p = (x[i],y[i]+step)
				double += [p]
				text(p[0],p[1], txt[i])
			else:
				text(x[i],y[i], txt[i])
				double += [(x[i],y[i])]


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
		self.graph_config(item1,item2, p1, p2, 'ro')
		self.plot_text(p1,p2, ob)
		show()

	def draw_items(self, object1, object2):
		p1 = []
		p2 = []
		k1 = set(self.ratings[object1].keys())
		k2 = set(self.ratings[object2].keys())
		u = k1.intersection(k2)
		items = list(u)

		p1 = [self.ratings[object1][item] for item  in items]
		p2 = [self.ratings[object2][item] for item  in items]
		
		self.graph_config(object1, object2, p1, p2, 'ro')
		self.plot_text(p1,p2,items)
		show()

if __name__ == '__main__':
	g = Recommendation(critics)
	print g.preferences
	print g.min_score, g.max_score
	#g.draw('Dupree','Snakes')
	#g.draw_items('Mick LaSalle','Gene Seymour')
	g.draw_items('Jack Matthews','Lisa Rose')
