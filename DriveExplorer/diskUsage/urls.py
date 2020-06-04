from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='homepage'),
    path('create', views.create, name='create_drive'),
    path('service/<str:id>/', views.service, name='service'),
    path('service', views.service, name='service'),
    path('upload', views.upload, name='upload'),
]
