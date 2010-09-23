from ci.calc.maths import *
from ci.data.critics import critics

def sim_distance(prefs,object1, object2):
	"""Returns a distance-based similarity score for object1 and object2"""
	shared_items = {}
	for item in prefs[object1]:
		if item in prefs[object2]:
			shared_items[item]=1

	if len(shared_items)==0: return 0

	values1 = [prefs[object1][item] for item in shared_items]
	values2 = [prefs[object2][item] for item in shared_items]

	return 1/(1+euclidean(values1,values2)**2)

if __name__ == "__main__":
	print sim_distance(critics,'Lisa Rose','Gene Seymour')
	print sim_distance(critics,'Lisa Rose','Lisa Rose')

        
