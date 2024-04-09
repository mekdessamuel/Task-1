from newscatcher import Newscatcher, describe_url
import json
import time

nyt = Newscatcher(website = 'nytimes.com')
results = nyt.get_news()

count = 0
articles = results['articles']
for article in articles[:10]:   
   count+=1
   print(
     str(count) + ". " + article["title"] \
     + "\n\t\t" + article["published"] \
     + "\n\t\t" + article["link"]\
     + "\n\n"
     )
   time.sleep(0.33)
