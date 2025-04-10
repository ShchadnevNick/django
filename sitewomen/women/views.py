from django.http import HttpResponse, HttpResponseNotFound, HttpResponsePermanentRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView

from women.forms import AddPostForm, UploadFileForm
from women.models import Women, Category, TagPost, UploadFiles
import uuid

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
]


class WomenHome(ListView):
    model = Women # Women.objects.all())
    template_name = 'women/index.html'
    context_object_name = 'posts'
    # Расширяем контекст шаблона
    def get_context_data(self, **kwargs):
        # Получаем базовый контекст (уже содержит posts=Women.objects.all())
        context = super().get_context_data(**kwargs)
        # Расширяем контекст шаблона
        context['title'] = 'Главная страница' # Заголовок страницы
        context['menu'] = menu # Предположительно список пунктов меню
        context['cat_selected'] = 0
        return context





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


class WomenCategory(ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat  # Берем категорию ПЕРВОЙ записи
        context['title'] = 'Категория - ' + cat.name  # Динамический заголовок
        context['menu'] = menu
        context['cat_selected'] = cat.id  # ID для подсветки
        return context

    def get_queryset(self):  # Берём только опубликованные записи
        return Women.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')


def archive(request, year):
    if year > 2025:
        url_redirect = reverse('cats', args=('music',))
        return HttpResponsePermanentRedirect(url_redirect)
    return HttpResponse(f'<h1>Архив по годам </h1> <h2>{year}</h2>')


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1> <h2>У вас ошибка</h2>")


class ShowPost(DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post']
        context['menu'] = menu
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Women.published, slug=self.kwargs[self.slug_url_kwarg])


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


class TagPostList(ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        context['title'] = 'Тег: ' + tag.tag
        context['menu'] = menu
        context['cat_selected'] = None
        return context

    def get_queryset(self):
        return Women.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')













