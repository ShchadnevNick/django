from django.http import HttpResponse, HttpResponseNotFound, HttpResponsePermanentRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, ListView

from women.forms import AddPostForm, UploadFileForm
from women.models import Women, Category, TagPost, UploadFiles
import uuid

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
]

class WomenHome(ListView):
    template_name = 'women/index.html'
    extra_context = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': Women.published.all().select_related('cat'),
        'cat_selected': 0,
    }



def handle_uploaded_file(f):
    name = f.name # Получаем оригинальное имя файла
    # Отделяем расширение от имени
    ext = ''
    if '.' in name:
        ext = name[name.rindex('.'):] # Берём всё после последней точки
        name = name[:name.rindex('.')] # Берём всё до последней точки
    # Генерируем случайный UUID
    suffix = str(uuid.uuid4()) # Н-р:'3b6f5f2d-8cae-4d9c-9fe8-7c3f5a1b0d4e'
    # Сохраняем файл с новым именем
    with open(f"uploads/{name}_{suffix}{ext}", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def about(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # handle_uploaded_file(form.cleaned_data['file'])
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm()

    return render(request, 'women/about.html', {'title': 'О сайте', 'menu': menu, 'form': form})


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


class AddPage(View):
    def get(self, request):
        form = AddPostForm()
        data = {'menu': menu, 'title': 'Добавление статьи', 'form': form}

        return render(request, 'women/addpage.html', data)

    def post(self, request):
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')

        data = {'menu': menu, 'title': 'Добавление статьи', 'form': form}

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












