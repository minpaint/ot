from django.urls import path
from . import views

app_name = 'departments'

urlpatterns = [
    path('by_organization/', views.get_departments_by_organization, name='get_departments'),
]
