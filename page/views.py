# coding=utf-8
from django.http import HttpResponse
from models import *


def index(request, cat_id):

    if cat_id is None:
        cat = Category.objects.first()
    else:
        cat = Category.objects.get(pk=cat_id)

    goods = Good.objects.filter(category=cat).order_by('name')
    s = u'Категория: ' + cat.name + '<br><br>'
    for good in goods:
        s = s + '(' + str(good.pk) + ') ' + good.name + '<br>'

    return HttpResponse(s)


def good(request, good_id):
    good = Good.objects.get(pk=good_id)
    s = good.name + '<br><br>' + good.category.name + '<br><br>' + good.description

    if not good.in_stock:
        s += '<br><br>' + 'Нет в наличии!'

    return HttpResponse(s)
