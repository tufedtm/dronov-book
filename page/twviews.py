from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from models import *


class GoodListView(ListView):
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
        contex = super(GoodListView, self).get_context_data(**kwargs)
        contex['categories'] = Category.objects.order_by('name')
        contex['category'] = self.category

        return contex

    def get_queryset(self):
        return Good.objects.filter(category=self.category).order_by('name')


class GoodDetailView(DetailView):
    template_name = 'good.html'
    model = Good
    pk_url_kwarg = 'good_id'

    def get_context_data(self, **kwargs):
        context = super(GoodDetailView, self).get_context_data(**kwargs)

        try:
            context['page_num'] = self.request.GET['page']
        except KeyError:
            context['page_num'] = 1

        context['categories'] = Category.objects.order_by('name')

        return context
