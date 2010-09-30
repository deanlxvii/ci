from ci.data.critics import critics

class Ratings(dict):
	"""
	Collection of ratings
	dictionair with key and values Rating
	"""
	def __init__(self, data=None):
		if data:
			self.format(data)

	def format(self, data):
		if type(data) == type(dict()):
			for id in data:
				_rating = Rating()
				for item in data[id]:
					_rating.rate(item, data[id][item])
				self.add(id, _rating)

	def add(self, id, rating):
		self.update({id:rating})

	@property
	def id(self):
		return self.keys()
	
	@property
	def ratings(self):
		return self.values()

class Rating(dict):
	"""
	A dictionair with an item that has a weight
	"""
	@property
	def items(self):
		return self.keys()
	
	@property
	def weights(self):
		return self.values()

	def rate(self, item, value):
		self.update({item:value})

	def __mul__(self, rating):
		_intersection = {}
		for item in self:
			if item in rating:
				_intersection[item] = 1
		return _intersection

if __name__ == "__main__":
	r = Rating()
	s = Rating()
	r.update(critics['Toby'])
	s.update(critics['Lisa Rose'])
	print r
	print r.items
	print r.weights
	x = r * s
	print x
	print type(r)
	print type(x)
	ratings= Ratings()
	ratings.add('Toby',r)
	ratings.add('Lisa Rose',s)
	print ratings
	print ratings['Toby']
	c = Ratings()
	c.format(critics)
	print len(c)


