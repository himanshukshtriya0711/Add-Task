# testcases/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('testcases/', views.test_cases, name='testcases'),
    path('add_test_cases/', views.add_test_cases, name='add_test_cases'),
    # Include the home view if you added it:
    path('', views.home, name='home'),
]
