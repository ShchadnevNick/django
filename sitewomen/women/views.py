from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, HttpResponsePermanentRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView, DeleteView
from women.forms import AddPostForm, UploadFileForm
from women.models import Women, TagPost, UploadFiles
import uuid

from women.utils import DataMixin, menu


class WomenHome(DataMixin, ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    # Расширяем контекст шаблона
    def get_queryset(self):
        return Women.published.all().select_related('cat')

    def get_context_data(self, **kwargs):
        return self.get_mixin_context(super().get_context_data(**kwargs),
                                      title='Главная страница',
                                      cat_selected=0, )


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

@login_required(login_url='/admin/')
def about(request):
    contact_list = Women.published.all()
    paginator = Paginator(contact_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'women/about.html', {'page_obj': page_obj, 'title': "О сайте" })


class WomenCategory(DataMixin, ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context,
                                      title='Категория - ' + cat.name,
                                      cat_selected=cat.id,)

    def get_queryset(self):  # Берём только опубликованные записи
        return Women.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')


def archive(request, year):
    if year > 2025:
        url_redirect = reverse('cats', args=('music',))
        return HttpResponsePermanentRedirect(url_redirect)
    return HttpResponse(f'<h1>Архив по годам </h1> <h2>{year}</h2>')


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1> <h2>У вас ошибка</h2>")


class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'])

    def get_object(self, queryset=None):
        return get_object_or_404(Women.published, slug=self.kwargs[self.slug_url_kwarg])


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    title_page = 'Добавление статьи'

    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


class TagPostList(DataMixin, ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, title='Тег: ' + tag.tag)


    def get_queryset(self):
        return Women.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')


class UpdatePage(UpdateView):
    model = Women
    fields = ['title', 'content', 'photo', 'is_published', 'cat']
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    extra_context = {
        'menu': menu,
        'title': 'Редактирование статьи',
    }

class DeletePage(DeleteView):
    model = Women  # Та же модель, что и в UpdateView
    template_name = 'women/deletepage.html'  # Шаблон подтверждения удаления
    success_url = reverse_lazy('home')  # Перенаправление на главную после удаления
    extra_context = {
        'menu': menu,  # То же меню, что и в других классах
        'title': 'Удаление статьи',  # Заголовок
    }


