from django.conf.urls import url
from twviews import *

urlpatterns = [
    url(r'^(?:(?P<cat_id>\d+)/)?$', GoodListView.as_view(), name='index'),
    url(r'^good/(?P<good_id>\d+)/$', GoodDetailView.as_view(), name='good'),
]
