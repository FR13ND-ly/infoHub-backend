from django.urls import path, include
from . import views

urlpatterns = [
    path('get/<str:url>', views.getComments),
    path('add/', views.addComment),
    path('remove/<int:id>', views.removeComment),
]