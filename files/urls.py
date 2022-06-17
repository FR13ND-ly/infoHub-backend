from django.urls import path, include
from . import views

urlpatterns = [
    path('<int:index>/', views.getFiles),
    path('add/', views.addFile),
    path('remove/<int:id>/', views.removeFile),
]