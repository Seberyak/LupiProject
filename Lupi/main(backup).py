import requests
import bs4
from .models import Posts, Routes
from threading import Thread
from random import randrange
from django.db.models.functions import Length
# res = requests.get("https://en.wikipedia.org/wiki/Heijō_Shrine")

all_urls = []
max_links = 5



# default url parameter is random wikipedia page
def scrap(url="https://en.wikipedia.org/wiki/Special:Random", step=1, ancestors="", last_ancestor=False):
    print(url)
    res = requests.get(url)
    main_id = 0
    # if res.url exist in Posts : return
    if Posts.objects.filter(url=res.url).exists():
        return

    try:
        # scrap page....
        soup = bs4.BeautifulSoup(res.text, 'lxml')
        heading = soup.find(id='firstHeading').get_text()
        content = soup.find('div', class_='mw-parser-output')

        # create post
        post = Posts(url=str(res.url), name=str(heading))
        # add post to Posts table
        post.save()
        main_id = post.id


    except:
        return

    # if len(ancestors) > 0 : save to Routes == url_main_id = last ancestor,
    # url_destination_id = post.id, route = ancestors
    if len(ancestors) > 0:

        route = Routes(main=last_ancestor, destination_id=post.id, ancestors=ancestors)

        if not Routes.objects.filter(ancestors=ancestors, main=route.main).exists():
            route.save()
    # add this url to ancestors for next recursion steps

    # scrap links, link format = https://en.wikipedia.org/...

    if step > 0:
        links = ["https://en.wikipedia.org" + link['href'] for link in content.find_all('a', href=True) if
                 '/wiki/' == link['href'][:6]]

        # temp lists for refreshable threads and urls
        threads = []
        temp_urls = []

        # get 5 random links
        links0 = []
        while len(links0) < max_links:
            r = randrange(len(links))
            if links[r] not in links0:
                links0.append(links[r])
                # print(links[r])
        try:
            for i in range(len(links0)):
                # anew url, step-1, ancestors, last_ancestor = post
                new_url = links0[i]
                if len(temp_urls) <= max_links and i < len(links0) - 1:
                    if new_url not in all_urls:
                        all_urls.append(new_url)
                        temp_urls.append(new_url)


                # run in 4 thread and wait
                else:

                    for link in temp_urls:
                        threads.append(Thread(target=scrap, args=(link, step - 1, ancestors + "{},".format(main_id), post)))

                    for thread in threads:
                        thread.start()

                    for thread in threads:
                        thread.join()

                    threads.clear()
                    temp_urls.clear()
        except:
            pass
    # add urls to global list

    # after all recursion step, return global list of scraped urls
    if not last_ancestor:
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


def calculate_way(id1, keyword):
    if Routes.objects.filter(ancestors__startswith=id1, main__name__icontains=keyword).exists():
        r = Routes.objects.filter(ancestors__startswith=id1, main__name__icontains=keyword).order_by(Length('ancestors'))
        return r[0].ancestors[:-1]
    else:
        return [['Nothing', '']]
