from django.shortcuts import render
from .models import Category, News

def index(request):
    ctg = Category.objects.all()
    news = News.objects.all().order_by('-date')
    latest_news = News.objects.all().order_by('-date')
    news_uzb = News.objects.filter(category=3)
    world_news = News.objects.filter(category__title = 'Jahon').order_by('-date')
    techno_news = News.objects.filter(category__title = 'Texnologiya').order_by('-date')
    sport = News.objects.filter(category__title = 'Sport').order_by('-date')

    images = (obj.image for obj in News.objects.all().order_by('-date'))

    context = {'ctg': ctg, 'news': news, 'latest_news': latest_news,
               'news_uzb': news_uzb, 'world_news': world_news, 'techno_news': techno_news, 'images': images, 'sport': sport }

    return render(request, 'index.html', context)


def contact(request):
    return render(request, 'contact.html')

def detail(request):
    return render(request, 'single_page.html')

def error_page(request):
    return render(request, '404.html')


