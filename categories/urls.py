from django.urls import path

from . import views

app_name = 'games'

urlpatterns = [
    path('', views.subject_list, name='subject-list'),
]
