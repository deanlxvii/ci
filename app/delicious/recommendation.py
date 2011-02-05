from ci.recommend import Recommendation as BaseRecommendation

class Recommendation(BaseRecommendation):
	def __init__(self, data):
		BaseRecommendation.__init__(self, data)

