from django.urls import path, include
from . import views

urlpatterns = [
    path('all/<int:index>/', views.getArticles),
    path('get-article-to-edit/<str:url>/', views.getArticleToEdit),
    path('drafts/', views.getDrafts),
    path('slider/', views.getSlider),
    path('right-side/', views.getRightSideArticles),
    path('category-articles/<str:tag>/', views.getCategoryArticles),
    path('edit/', views.editArticle),
    path('search/', views.search),
    path('survey/', views.getSurvey),
    path('vote/', views.vote),
    path('aditional-articles/<str:url>/', views.getAditionalArticles),
    path('delete/<str:url>/', views.deleteArticle),
    path('next-article/', views.nextArticle),
    path('<str:url>/', views.getArticle),
]