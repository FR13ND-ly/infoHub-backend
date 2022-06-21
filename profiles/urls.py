from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.login),
    path('authorization/<str:token>/', views.getUserAuthorization),
    path('set-user-image/<str:token>/', views.setUserImage),
    path('all/', views.getAllUsers),
    path('update/', views.updateUser),
    path('default-avatar/<int:id>/', views.setDefaultAvatar),
    path('delete/<int:id>/', views.deleteUser)
]