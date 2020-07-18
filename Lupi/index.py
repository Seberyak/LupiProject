from django.http import HttpResponse
from  django.shortcuts import render


#task1
def scrap_wiki(request):
    return render(request, 'scrap_wiki.html')

#task2
def find_page(request):
    return HttpResponse("Input word to find  page of departure ")

def list_page(request):
    return HttpResponse("List of wikipedia page-s ")

def destination_page(requset):
    return HttpResponse("Input word to find page of destination")

def latest_response(request):
    return HttpResponse("Distance in clicks between the pages")