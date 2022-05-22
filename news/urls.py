from django.urls import path
from . import views


urlpatterns = [
    path('', views.MainPage.as_view()),
    path('news/', views.NewsPage.as_view()),
    path('news/create/', views.CreatePage.as_view()),
    path('news/<int:link>/', views.SomeNewPage.as_view())
]
