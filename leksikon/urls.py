from django.urls import path
from leksikon import views

# All urls that start with "leksikon/"
urlpatterns = [
    path('', views.hello_world)
]
