from django.urls import path, include
from . import views

urlpatterns = [
    path('get/all/', views.getWidgets),
    path('get/<str:id>/', views.getWidget),
    path('edit/<str:id>/', views.editWidget)
]