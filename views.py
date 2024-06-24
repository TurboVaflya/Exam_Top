from django.http import HttpResponse, HttpResponseNotFound, HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.decorators.http import require_GET
from . import forms
from . import models

from django.template.loader import render_to_string


menu = [
        {'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Регистрация", 'url_name': 'register'},
        {'title': "Войти", 'url_name': 'login_p'},
    ]

data_db = [
    {'id': 1, 'title': 'Эрмитаж', 'content': 'Эрмитаж — один из крупнейших и старейших музеев мира, расположенный в самом сердце Санкт-Петербурга. Он является гордостью не только города, но и всей России, привлекая туристов со всего мира своими богатыми коллекциями и великолепной архитектурой. История музея: Основанный в 1764 году по приказу императрицы Екатерины Великой, Эрмитаж начинался как частная галерея, в которой хранились коллекции живописи. С тех пор музей неуклонно рос и развивался, и сегодня его коллекция насчитывает более трех миллионов экспонатов, включая произведения живописи, скульптуры, графики, нумизматики и археологии. Эта статья может быть использована для привлечения внимания к Эрмитажу на туристическом сайте "Вместе". Если вам нужны дополнительные материалы или есть другие запросы, пожалуйста, сообщите мне!', 'is_published': True},
    {'id': 2, 'title': 'Рускеальский Парк', 'content': 'Посещение Рускеальского национального парка стало одним из самых ярких впечатлений моей жизни. Это место, где природа показывает свою необузданную красоту и мощь. Мраморный каньон, с его скалистыми стенами и чистейшей водой, заставляет забыть обо всем на свете. Прогулка по парку — это как путешествие в другой мир, где каждый шаг открывает новые удивительные виды. Этот отзыв может быть опубликован на туристическом сайте "Вместе" для того, чтобы поделиться личным опытом посещения Рускеальского национального парка с будущими посетителями. Если вам нужны дополнительные изменения или есть другие запросы, пожалуйста, дайте мне знать!', 'is_published': True},
    {'id': 3, 'title': 'Дом Горького в Нижнем Новгороде', 'content': 'Дом Горького в Нижнем Новгороде, также известный как Музей-усадьба А.М. Горького, является одним из самых значимых мест в городе, связанных с жизнью и творчеством великого русского писателя. Этот дом, в котором писатель провел свои юношеские годы, представляет собой яркий пример гражданской архитектуры конца XIX века и является памятником федерального значения. Этот обзор может быть использован для публикации на туристическом сайте "Вместе" или в любом другом ресурсе, посвященном культурному наследию и истории России. Если вам нужна дополнительная информация или есть другие запросы, пожалуйста, дайте мне знать!', 'is_published': True},
]

cats_db = [
    {'id': 1, 'name': 'Статьи'},
    {'id': 2, 'name': 'Отзывы'},
    {'id': 3, 'name': 'Обзоры'},
]


def index(request):
    # t = render_to_string('Saratov/index.html')
    # return HttpResponse(t)
    data = {
        'title': 'Вместе',
        'menu': menu,
        'posts': list(models.BlogMessage.objects.all()),
        'cat_selected': 0,
    }
    return render(request, 'Saratov/index.html', context=data)


def about(request):
    return render(request, 'Saratov/about.html', {'title': '"Вместе" - платформа для путешественников и их историй. Откройте для себя мир через рассказы и статьи наших пользователей. "Вместе" - это не просто туристический сайт, это сообщество единомышленников, где каждый может поделиться своими впечатлениями и открытиями. У вас было незабываемое путешествие и вы хотите рассказать о нем миру? На "Вместе" вы можете оставить свою статью и советы для других путешественников. Ваш опыт поможет другим найти вдохновение для новых приключений!', 'menu': menu})


def categories(request, cat_id):
    return HttpResponse(f"<h1>Страница по категориям</h1><p>id:{cat_id}</p>")


def categories_by_slug(request, cat_slug):
    if request.GET:
        print(request.GET)
    return HttpResponse(f"<h1>Страница по категориям</h1><p>slug:{cat_slug}</p>")


def show_post(request, post_id):
    data = {
        'title': 'Вместе',
        'menu': menu,
        'posts': list(models.BlogMessage.objects.filter(pk=post_id)),
        'cat_selected': 0,
    }
    return render(request, 'Saratov/single.html', context=data)


def contact(request):
    return HttpResponse("https://vk.com/plumstalker")


def show_category(request, cat_id):
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': data_db,
        'cat_selected': cat_id,
    }
    return render(request, 'Saratov/index.html', context=data)


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


def register(request: HttpRequest):

    # -- GET --
    if request.method == 'GET':
        from_kwargs = {'form': forms.UserFormRegister()}
        return render(request, 'Saratov/register_page.html', from_kwargs)

    # -- POST --
    reg_form = forms.UserFormRegister(request.POST)

    if not reg_form.is_valid():
        return redirect(register)

    username = reg_form.cleaned_data.get('username')
    if models.User.objects.filter(username=username).exists():
        messages.info(request, 'Имя пользователя занято')
        return redirect(register)

    user = reg_form.save()
    user.set_password(reg_form.cleaned_data.get('password'))
    user.save()

    return redirect(login_p)


def login_p(request: HttpRequest):
    # -- GET --
    if request.method == 'GET':
        template_kwargs = { 'form': forms.UserFormLogin() }
        return render(request, 'Saratov/login_page.html', template_kwargs)

    # -- POST --
    login_form = forms.UserFormLogin(request.POST)

    if not login_form.is_valid():
        return redirect( login_p, errors=login_form.errors )

    password = login_form.cleaned_data.get('password')
    username = login_form.cleaned_data.get('username')

    if not models.User.objects.filter(username=username).exists():t
        messages.info(request, 'Неверное имя пользователя!')
        return redirect( login_p )

    user = authenticate(request, password=password, username=username)

    if user is None:
        messages.info(request, 'Неверный пароль!')
        return redirect( login_p )

    login(request, user)
    return redirect( index )


def add_blog(request: HttpRequest):
    # -- GET --
    if request.method == 'GET':
        blog_form = forms.BlogForm()
        from_kwargs = {'form': blog_form}
        return render(request, 'Saratov/add_blog.html', from_kwargs)

    # -- POST --
    blog_form = forms.BlogForm(request.POST, sender=request.user)
    if blog_form.is_valid():
        blog_form.save()
        return redirect( index )

    return redirect( add_blog )
