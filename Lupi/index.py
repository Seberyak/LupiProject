from django.http import HttpResponse
from django.shortcuts import render
from .main import *


# task1

def main(request):
    context = dict()
    context['links_count'] = 0
    if 'url' in request.POST.keys() and 'step' in request.POST.keys() and len(request.POST['step']) > 0:
        scraped_links = scrap(request.POST['url'], int(request.POST['step']))
        context = scraped_links

    return render(request, 'scrap_input.html', context=context)


def scraped_wiki_pages(request):
    # print(request.POST.keys())
    return render(request, "url for scrap:")


# task2
def find_page(request):
    context = dict()
    if 'keyword' in request.POST.keys():
        if len(request.POST['keyword']) > 0:
            context['posts'] = find_post(request.POST['keyword'])
            context['direct'] = "/destination?main="
    return render(request, 'find_page.html', context)


def destination_page(request):
    context = {}
    main_id = 0
    if 'main' in request.GET.keys():
        main_id = request.GET['main']
    if 'keyword' in request.POST.keys():
        keyword = request.POST['keyword']
        route = calculate_way(main_id, keyword)
        try:
            # ids = route.split(',')
            context['route'] = [find_by_id(i) for i in route]
            print(context['route'])
        except:
            pass

        # print(type(main_id), type(keyword))
    return render(request, 'Closest_way.html', context)
