from django.urls import path
from . import views

urlpatterns = [
    path('testcases', views.testcases_view, name='testcases'),
    path('add_test_cases', views.add_test_cases, name='add_test_cases'),
]
