from django.urls import path
from blogs import views

urlpatterns = [
    path('', views.index, name='home'),
    path('post_details/', views.post_details, name='post_details'),
    path('post_new/', views.post_new, name='post_new'),
]