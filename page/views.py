# coding=utf-8
from django.shortcuts import render
from models import *


def index(request, cat_id):
    categories = Category.objects.all().order_by('name')

    if cat_id is None:
        cat = Category.objects.first()
    else:
        cat = Category.objects.get(pk=cat_id)

    goods = Good.objects.filter(category=cat).order_by('name')

    return render(request, 'index.html', {'category': cat, 'categories': categories, 'goods': goods})


def good(request, good_id):
    categories = Category.objects.all().order_by('name')
    good_item = Good.objects.get(pk=good_id)

    return render(request, 'good.html', {'good_item': good_item, 'categories': categories})
