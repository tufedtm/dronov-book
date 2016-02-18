from django.views.generic.base import ContextMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from models import *


class CategoryListMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super(CategoryListMixin, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.order_by('name')

        return context


class GoodListView(ListView, CategoryListMixin):
    template_name = 'index.html'
    paginate_by = 2

    category = None

    def get(self, request, *args, **kwargs):

        if self.kwargs['cat_id'] is None:
            self.category = Category.objects.first()
        else:
            self.category = Category.objects.get(pk=kwargs['cat_id'])

        return super(GoodListView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GoodListView, self).get_context_data(**kwargs)
        context['category'] = self.category

        return context

    def get_queryset(self):
        return Good.objects.filter(category=self.category).order_by('name')


class GoodDetailView(DetailView, CategoryListMixin):
    template_name = 'good.html'
    model = Good
    pk_url_kwarg = 'good_id'

    def get_context_data(self, **kwargs):
        context = super(GoodDetailView, self).get_context_data(**kwargs)

        try:
            context['page_num'] = self.request.GET['page']
        except KeyError:
            context['page_num'] = 1

        return context
