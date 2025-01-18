from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'documents'

router = DefaultRouter()
router.register(r'', views.DocumentViewSet, basename='document')

urlpatterns = [
    path('', include(router.urls)),
]