from django.conf.urls import url
from demoproject.web.views import *

urlpatterns = [
    url(r'^$', HomePageView.as_view(), name='home')
]
