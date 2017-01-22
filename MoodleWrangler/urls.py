from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.LoginPageView.as_view(), name='login'),
    url(r'^home/', views.HomePageView.as_view(), name='home')
]
