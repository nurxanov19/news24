from django.shortcuts import render, redirect
from .models import Category, News, Contact
from datetime import datetime
from .forms import ContactForm
from django.contrib import messages


def get_date():
    return datetime.today()

def get_categories():
    return Category.objects.all()

def index(request):

    news = News.objects.all().order_by('-date')
    latest_news = News.objects.all().order_by('-date')
    news_uzb = News.objects.filter(category=3)
    world_news = News.objects.filter(category__title = 'Jahon').order_by('-date')
    techno_news = News.objects.filter(category__title = 'Texnologiya').order_by('-date')
    sport = News.objects.filter(category__title = 'Sport').order_by('-date')
    popular_news = News.objects.all().order_by('views')

    images = (obj.image for obj in News.objects.all().order_by('-date'))

    context = {'ctg': get_categories(), 'news': news, 'latest_news': latest_news,
               'news_uzb': news_uzb, 'world_news': world_news, 'techno_news': techno_news, 'images': images, 'sport': sport,
               'date': get_date(), "popular_news": popular_news[:4] }

    return render(request, 'index.html', context)


def contact(request):
    news = News.objects.all().order_by('-date')
    popular_news = News.objects.all().order_by('views')

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message sent successfully')
            return redirect('contact')

        else: messages.error(request, 'Oops, something went wrong')
    else: form = ContactForm()

    context = {
        'news': news,
        'popular_news': popular_news,
        'ctg': get_categories(),
        'form': form,
    }

    return render(request, 'contact.html', context)


def detail(request, pk):
    new = News.objects.get(pk=pk)
    news = News.objects.filter(category__title=new.category).order_by('-date')
    popular_news = News.objects.filter(category__title=new.category).order_by('views')
    new.views += 1
    new.save()

    context = {
        'new': new,
        'news': news[:4],
        'popular_news': popular_news,
        'ctg': get_categories(),
        'date': get_date(),
    }
    return render(request, 'single_page.html', context)


def error_page(request):
    return render(request, '404.html')

def category(request, pk):
    ctg = Category.objects.get(pk=pk)
    news = News.objects.filter(category__title=ctg.title).order_by('-date')
    print(news)
    context = {
        'ctg': get_categories(),
        'news': news,
        'date': get_date(),
    }
    return render(request, 'category.html', context)


