import requests
import bs4
from .models import Posts, Routes
from threading import Thread
from random import randrange
from django.db.models.functions import Length

# res = requests.get("https://en.wikipedia.org/wiki/Heijō_Shrine")

max_links = 5
all_urls = []


def scrap(url="https://en.wikipedia.org/wiki/Special:Random", step=1, parent=-1):
    res = requests.get(url)

    try:
        # scrape page
        soup = bs4.BeautifulSoup(res.text, 'lxml')
        heading = soup.find(id='firstHeading').get_text()

        if Posts.objects.filter(url=res.url, name=heading).exists():
            return

        content = soup.find('div', class_='mw-parser-output')

        all_urls.append(res.url)

        post = Posts(url=str(res.url), name=str(heading))
        post.save()

        route = Routes(main_id=parent, destination_id=post.id)
        route.save()

    except Exception as e:
        print(e)
        return

    if step == 0:
        return

    links = ["https://en.wikipedia.org" + link['href'] for link in content.find_all('a', href=True) if
             '/wiki/' == link['href'][:6]]
    links = links[:min(max_links, len(links))]
    threads = []
    for link in links:
        threads.append(Thread(target=scrap, args=(link, step - 1, post.id)))
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    threads.clear()

    # after all steps, recursion backs to root and return all scraped pages
    if parent == -1:
        context = dict()
        context['links_count'] = len(all_urls)
        context['links'] = all_urls.copy()
        all_urls.clear()
        return context


def find_post(keyword):
    posts = Posts.objects.filter(name__icontains=keyword)
    return list(posts)


def find_by_id(this_id):
    p = Posts.objects.get(pk=this_id)
    return [p.name, p.url]


def find_shortest_way(searching_id, id2, ancestors=[]):
    searching_id, id2 = int(searching_id), int(id2)
    destinations = Routes.objects.filter(destination_id=id2)
    for i in destinations:
        # if found
        if i.main_id == searching_id:
            # print((ancestors+[searching_id])[::-1])
            return (ancestors+[searching_id])[::-1]
        # if it is not root and id doesn't equals searching id
        elif i.main_id != searching_id and i.id != '-1':
            return find_shortest_way(searching_id, i.main_id, ancestors + [i.main_id])
        # else:
        #     return


def calculate_way(id1, keyword, marked_posts=[]):
    posts = Posts.objects.filter(name__icontains=keyword)
    routes = []
    for i in posts:
        id2 = i.id
        l = find_shortest_way(id1, id2)
        if type(l)==list:
            if len(l)>0:
                # print(l)
                routes.append(l)
    if len(routes) > 0:
        return min(routes)+[id2]
    else:
        return "Nothing"
