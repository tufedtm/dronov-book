# coding: utf8

from __future__ import unicode_literals
from django.db import models


class Category(models.Model):
    name = models.CharField('Название', max_length=30, unique=True)
    description = models.TextField('Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Good(models.Model):
    name = models.CharField('Название', max_length=50, unique=True)
    description = models.TextField('Описание')
    in_stock = models.BooleanField('В наличии', default=True, db_index=True)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        s = self.name
        if not self.in_stock:
            s += ' (нет в наличии)'
        return s

    def get_in_stock(self):
        if self.in_stock:
            return '+'
        else:
            return ''

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class BlogArticle(models.Model):
    name = models.CharField(max_length=50, unique_for_month='pubdate')
    pubdate = models.DateField()
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
