# coding=utf-8
from django import forms
from django.core.urlresolvers import reverse
from django.views.generic.base import ContextMixin
from django.views.generic.edit import CreateView, DeleteView, ProcessFormView, UpdateView
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


class GoodEditMixin(CategoryListMixin):
    def get_context_data(self, **kwargs):
        context = super(GoodEditMixin, self).get_context_data(**kwargs)

        try:
            context['page_num'] = self.request.GET['page']
        except KeyError:
            context['page_num'] = 1

        return context


class GoodEditView(ProcessFormView):
    def post(self, request, *args, **kwargs):

        try:
            page_num = request.GET['page']
        except KeyError:
            page_num = 1

        self.success_url = self.success_url + '?page=' + page_num

        return super(GoodEditView, self).post(request, *args, **kwargs)


class GoodForm(forms.ModelForm):

    class Meta:
        model = Good
        fields = '__all__'

    # name = forms.CharField()
    # description = forms.CharField()
    # category = forms.ModelChoiceField(Category.objects.all())
    # in_stock = forms.BooleanField()


class GoodCreate(CreateView, GoodEditMixin):
    model = Good
    template_name = 'good_add.html'
    form_class = GoodForm

    def get(self, request, *args, **kwargs):
        if self.kwargs['cat_id'] is not None:
            self.initial['category'] = Category.objects.get(pk=self.kwargs['cat_id'])

        return super(GoodCreate, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.success_url = reverse('index',
                                   kwargs={'cat_id': Category.objects.get(pk=self.kwargs['cat_id'].id)})

        return super(GoodCreate, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GoodCreate, self).get_context_data(**kwargs)
        context['category'] = Category.objects.get(pk=self.kwargs['cat_id'])

        return context


class GoodUpdate(UpdateView, GoodEditMixin, GoodEditView):
    model = Good
    template_name = 'good_edit.html'
    pk_url_kwarg = 'good_id'
    form_class = GoodForm

    def post(self, request, *args, **kwargs):
        self.success_url = reverse('index',
                                   kwargs={'cat_id': Category.objects.get(pk=self.kwargs['good_id'])}
                                   )
    
        return super(GoodUpdate, self).post(request, *args, **kwargs)


class GoodDelete(DeleteView, GoodEditMixin, GoodEditView):
    model = Good
    template_name = 'good_delete.html'
    pk_url_kwarg = 'category_id'

    def post(self, request, *args, **kwargs):
        self.success_url = reverse('index',
                                   kwargs={'cat_id': Category.objects.get(pk=self.kwargs['category_id'])})

        return super(GoodDelete, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GoodDelete, self).get_context_data(**kwargs)
        context['good'] = Good.objects.get(pk=self.kwargs['good_id'])

        return context
