from django.conf.urls import url
from twviews import *

urlpatterns = [
    url(r'^(?:(?P<cat_id>\d+)/)?$', GoodListView.as_view(), name='index'),
    url(r'^good/(?P<good_id>\d+)/$', GoodDetailView.as_view(), name='good'),
    url(r'^(?P<cat_id>\d+)/add$', GoodCreate.as_view(), name='good_add'),
    url(r'^good/(?P<good_id>\d+)/edit', GoodUpdate.as_view(), name='good_edit'),
    url(r'^good/(?P<good_id>\d+)/delete', GoodDelete.as_view(), name='good_delete')
]
