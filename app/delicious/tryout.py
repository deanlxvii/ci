from ci.app.delicious.scraper import TagItem
from ci.lib.calc.maths import *
from ci.app.delicious.recommendation import Recommendation


scraper = TagItem()
scraper.initialize_object_dict('programming')
scraper.fill_items()

recommend = Recommendation(scraper.object_dict)
