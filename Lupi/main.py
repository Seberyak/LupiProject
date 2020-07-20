import requests
import bs4
from .models import Posts, Routes
from threading import Thread
from random import randrange
from django.db.models.functions import Length

# res = requests.get("https://en.wikipedia.org/wiki/Heijō_Shrine")

max_links = 5


def scrap(url="https://en.wikipedia.org/wiki/Special:Random", step=1, parent=False):
    res = requests.get(url)
    if Posts.objects.filter(url=res.url).exists():
        return
    try:
        # scrap page....
        soup = bs4.BeautifulSoup(res.text, 'lxml')
        heading = soup.find(id='firstHeading').get_text()
        content = soup.find('div', class_='mw-parser-output')

        post = Posts(url=str(res.url), name=str(heading))
        post.save()

        route = Routes(main_id=parent, destination_id=post.id)
        route.save()

    except Exception:
        print(Exception)
        return

    if step == 0:
        return

    links = ["https://en.wikipedia.org" + link['href'] for link in content.find_all('a', href=True) if
             '/wiki/' == link['href'][:6]]
    links = links[:min(max_links, len(links))]
    threads = []
    for link in links:
        threads.append(Thread(target=scrap, args=(link, step-1, post)))


def find_post(keyword):
    posts = Posts.objects.filter(name__icontains=keyword)
    return list(posts)


def find_by_id(this_id):
    p = Posts.objects.get(pk=this_id)
    return [p.name, p.url]


def calculate_way(id1, keyword):
    if Routes.objects.filter(ancestors__startswith=id1, main__name__icontains=keyword).exists():
        r = Routes.objects.filter(ancestors__startswith=id1, main__name__icontains=keyword).order_by(
            Length('ancestors'))
        return r[0].ancestors[:-1]
    else:
        return [['Nothing', '']]
