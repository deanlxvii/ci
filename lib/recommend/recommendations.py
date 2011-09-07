from math import sqrt
from ci.lib.calc.maths import *
from ci.lib.recommend.ratings import *

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


    def get_tanimoto_recommendations(self, object, function):
        totals = {}
        similar_sums = {}
        for other_object in self.preferences:
            if other_object == object: continue
            similar = self.similarity(function, object, other_object)

            if similar <= 0: continue
            for item in self.preferences[other_object]:
                if item not in self.preferences[object] or self.preferences[object][item] == []:
                    totals.setdefault(item,0)
                    totals[item]+=1
                    similar_sums.setdefault(item,0)
                    similar_sums[item]+=similar

        # Create normilized list
        rankings = [(total/similar_sums[item],item) for item, total in totals.items()]
        rankings.sort()
        rankings.reverse()
        return rankings


    def get_recommendations(self, object, function):
        """
        Get recommendations for an object by using a weighted average
        of every object's ranking
        """
        
        if function.__name__ == 'tanimoto':
            return self.get_tanimoto_recommendations(object, function)

        totals = {}
        similar_sums = {}
        for other_object in self.preferences:
            if other_object == object: continue
            similar = self.similarity(function, object, other_object)

            # ignore scores equal or lower then zero
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

    def reverse(self):
        """
        swap the object and items in the preferences
        """
        result = dict()
        for object in self.preferences:
            for item in self.preferences[object]:
                result.setdefault(item,{})
                # swap item and object
                result[item][object]=self.preferences[object][item]
        return result

    def calculate_similar_items(self, n=10):
        """
        Create a dictionary of items showing which other items they
        are most similar to.
        """
        result = dict()

        # Invert the preference matrix to be item-centric
        item_recommend = Recommendation(self.reverse())
        c = 0
        for item in item_recommend.preferences:
            # Status updates for large datasets
            c+=1
            if c%100==0: print "%d / %d" (c, len(item_recommend.preferences))
            # Find the most similar items to this one
            scores = item_recommend.top_matches(item, n=n, function=euclidean)
            result[item]=scores
        return result

    def get_recommended_items(self, item_match, object):
        user_ratings = dict(self.preferences[object])
        scores = dict()
        total_similar = dict()

        # Loop over items rated by this object
        for (item, rating) in user_ratings.items():

            # Loop over items similar to this one
            for (similarity, item2) in item_match[item]:

                # Ignore if this user has already rated this item
                if item2 in user_ratings: continue

                # Weighted sum of rating times similarity
                scores.setdefault(item2,0)
                scores[item2] += similarity * rating

                # Sum of all the similarities
                total_similar.setdefault(item2,0)
                total_similar[item2] += similarity

        # Divide each total score by total weighting to get an average
        rankings = [(score/total_similar[item], item) for item, score in scores.items()]

        # Return the rankings from highest to lowest
        rankings.sort()
        rankings.reverse()
        return rankings
