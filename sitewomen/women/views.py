from django.http import HttpResponse, HttpResponseNotFound, HttpResponsePermanentRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from women.forms import AddPostForm
from women.models import Women, Category, TagPost


menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
]

def index(request):
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': Women.published.all().select_related('cat'),
        'cat_selected': 0,
    }
    return render(request, 'women/index.html', data)


def about(request):
    data = {
        'title': 'О сайте',
        'menu': menu,
    }
    return render(request, 'women/about.html', data)


def categories(request, cat_slug):
    return HttpResponse(f'Страница с категорией: {cat_slug}')


def archive(request, year):
    if year > 2025:
        url_redirect = reverse('cats', args=('music',))
        return HttpResponsePermanentRedirect(url_redirect)
    return HttpResponse(f'<h1>Архив по годам </h1> <h2>{year}</h2>')


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1> <h2>У вас ошибка</h2>")


def show_post(request, post_slug):
    post = get_object_or_404(Women, slug=post_slug)
    return render(request, 'women/post.html', {'post': post} )


def addpage(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AddPostForm()
        
    data = {
        'menu': menu,
        'title': 'Добавление статьи',
        'form': form
    }
    return render(request, 'women/addpage.html', data)


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Women.published.filter(cat_id=category.pk).select_related("cat")
    data = {
        'title': f'Рубрика: {category.name}',
        'menu': menu,
        'posts': posts,
        'cat_selected': category.pk,
    }
    return render(request, 'women/index.html', data)


def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=Women.Status.PUBLISHED).select_related("cat")
    data = {
        'title': f'Тег:{tag.tag}',
        'menu': menu,
        'posts': posts,
        'cat_selected': None,
    }

    return render(request, 'women/index.html', data)












