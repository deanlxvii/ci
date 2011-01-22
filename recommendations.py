from math import sqrt
from ci.calc.maths import *
from ci.ratings import *

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
                self.preferences = Ratings(data)

    @property
    def ratings(self):
        return self.preferences

    def empty(self,intersection):
        if len(intersection) == 0:
            return True
        return False

    def euclidean_correction(self, value):
        return 1/(1+value**2)

    def similarity(self, function, object1, object2):
        shared_items = self.ratings[object1] * self.ratings[object2]
        if self.empty(shared_items):
            return 0
        weights1 = [self.ratings[object1][item] for item in shared_items]
        weights2 = [self.ratings[object2][item] for item in shared_items]
        
        if function.__name__ == 'euclidean':
            return self.euclidean_correction(function(weights1, weights2))
        return function(weights1, weights2)

    def top_matches(self, object, function, n=5):
        scores = [(self.similarity(function,object,other_object), other_object)
                for other_object in self.preferences if other_object != object]

        # Sort the list so the highest score appear at the top
        scores.sort()
        scores.reverse()
        return scores[0:n]

    def get_recommendations(self, object, function):
        """
        Get recommendations for an object by using a weighted average
        of every object's ranking
        """
        totals = {}
        similar_sums = {}
        for other_object in self.preferences:
            if other_object == object: continue
            similar = self.similarity(function, object, other_object)

            if similar <= 0: continue
            for item in self.preferences[other_object]:
                if item not in self.preferences[object] or self.preferences[object][item]==0:
                    totals.setdefault(item,0)
                    totals[item]+=self.preferences[other_object][item]*similar
                    similar_sums.setdefault(item,0)
                    similar_sums[item]+=similar

        # Create normilized list
        rankings = [(total/similar_sums[item],item) for item, total in totals.items()]
        rankings.sort()
        rankings.reverse()
        return rankings
