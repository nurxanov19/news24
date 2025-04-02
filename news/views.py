from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now

from .models import Category, News, Contact
from datetime import datetime
from .forms import ContactForm, CommentForm
from django.contrib import messages
from user.models import Comment


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
    comments = Comment.objects.filter(post__title = new.title).order_by('-created_at')
    post = None
    editing_comment = request.GET.get('edit_comment', None)

    if request.POST:
        post_id = request.POST.get('post_id')

        if post_id:
            post = get_object_or_404(Comment, id=post_id)
            if post.like.filter(id=request.user.id):
                post.like.remove(request.user)
            else:
                post.like.add(request.user)

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = new
            comment.save()
            return redirect('detail', pk=new.pk)
    else: form = CommentForm()

    new.views += 1
    new.save()

    context = {
        'new': new,
        'news': news[:4],
        'popular_news': popular_news,
        'ctg': get_categories(),
        'date': get_date(),
        'form': form,
        'comments': comments,
        'post': post,
        'user': request.user,
        'editing_comment': int(editing_comment) if editing_comment else None,
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


from django.utils.timezone import now

def edit_comment(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    new = get_object_or_404(News, pk=comment.post.pk)  # Ensure correct News instance

    if comment.user != request.user:
        return redirect('detail', pk=new.pk)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.edited_at = now()  # Update the timestamp
            comment.save()
            return redirect('detail', pk=new.pk)

    else:
        form = CommentForm(instance=comment)

    return render(request, 'single_page.html', {
        'comments': Comment.objects.filter(post=new).order_by('-created_at'),
        'new': new,
        'editing_comment': comment.id,
        'user': request.user,
        'form': form,
    })
