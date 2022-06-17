from django.urls import path, include
from . import views

urlpatterns = [
    path('get/', views.getLikes),
    path('interact/', views.addLike),
]