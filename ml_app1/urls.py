from django.urls import path
from ml_app1 import views

app_name = 'ml_app1'
urlpatterns = [
    path('', views.index, name='index'),
    path('result', views.result, name='result'),
]

