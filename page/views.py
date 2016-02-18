# coding=utf-8
from django.shortcuts import render
from models import *
from django.core.paginator import Paginator, InvalidPage


def index(request, cat_id):
    categories = Category.objects.all().order_by('name')

    try:
        page_num = request.GET['page']
    except KeyError:
        page_num = 1

    if cat_id is None:
        cat = Category.objects.first()
    else:
        cat = Category.objects.get(pk=cat_id)

    paginator = Paginator(Good.objects.filter(category=cat).order_by('name'), 2)

    try:
        goods = paginator.page(page_num)
    except InvalidPage:
        goods = paginator.page(1)

    return render(request, 'index.html', {'category': cat, 'categories': categories, 'goods': goods})


def good(request, good_id):
    categories = Category.objects.all().order_by('name')

    try:
        page_num = request.GET['page']
    except KeyError:
        page_num = 1

    good_item = Good.objects.get(pk=good_id)

    return render(request, 'good.html', {'good_item': good_item, 'categories': categories, 'page_num': page_num})
