import requests
import bs4
from django.db import models
from .models import Posts,Routes

# res = requests.get("https://en.wikipedia.org/wiki/Heijō_Shrine")

# default url parameter is random wikipedia page
def scrap(url="https://en.wikipedia.org/wiki/Special:Random", step=0, ancestors=[], last_ancestor=False):
    res = requests.get(url)

    # if res.url exist in Posts : return
    if Posts.objects.filter(url=res.url).exists():
        return

    try:
        # scrap page....
        soup = bs4.BeautifulSoup(res.text, 'lxml')
        heading = soup.find(id='firstHeading')
        content = soup.find(id='bodyContent')

        # create post
        post = Posts(url=res.url, name=heading)
        # add to Posts table
        post.save()

    except:
        return

    # if len(ancestors) > 0 : save to Routes == url_main_id = last ancestor,
    # url_destination_id = post.id, route = ancestors
    if len(ancestors) > 0:
        route = Routes(url_main_id=last_ancestor, url_destination_id=post.id, ancestors=ancestors)

    # add this url to ancestors for next recursion steps
    ancestors.append(res.url)

    # scrap links, link format = https://en.wikipedia.org/...
    links = ["https://en.wikipedia.org" + link['href'] for link in soup.find_all('a', href=True) if
             '/wiki/' == link['href'][:6]]

    if step > 0:
        for new_url in links:
            # anew url, step-1, ancestors, last_ancestor = post
            scrap(new_url, step - 1, ancestors, post)
