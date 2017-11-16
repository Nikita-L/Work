from django.conf.urls import url
from .views import MainTemplateView

app_name = 'tires'
urlpatterns = [
    url(r'^$', MainTemplateView.as_view(), name='main'),
]
