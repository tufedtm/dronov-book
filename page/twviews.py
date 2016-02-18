from django.core.paginator import Paginator, InvalidPage
from django.http import Http404
from django.views.generic.base import TemplateView
from models import *


class GoodListView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(GoodListView, self).get_context_data(**kwargs)

        try:
            page_num = self.request.GET['page']
        except KeyError:
            page_num = 1

        context['categories'] = Category.objects.all().order_by('name')

        if kwargs['cat_id'] is None:
            context['category'] = Category.objects.first()
        else:
            context['category'] = Category.objects.get(pk=kwargs['cat_id'])

        paginator = Paginator(Good.objects.filter(category=context['category']).order_by('name'), 2)

        try:
            context['goods'] = paginator.page(page_num)
        except InvalidPage:
            context['goods'] = paginator.page(1)

        return context


class GoodDetailView(TemplateView):
    template_name = 'good.html'
    
    def get_context_data(self, **kwargs):
        context = super(GoodDetailView, self).get_context_data(**kwargs)

        try:
            context['page_num'] = self.request.GET['page']
        except KeyError:
            context['page_num'] = 1

        context['categories'] = Category.objects.all().order_by('name')

        try:
            context['good_item'] = Good.objects.get(pk=context['good_id'])
        except Good.DoesNotExist:
            raise Http404

        return context
