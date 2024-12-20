from django.urls import path , include
from . import views
from rest_framework.routers import DefaultRouter
from .views import HotelViewSet , PlaceViewSet




router = DefaultRouter()
router.register(r'hotels', HotelViewSet, basename='hotel')
router.register(r'places', PlaceViewSet, basename='place')

urlpatterns = [
   path('test' , views.test_main ) , 
   path('', include(router.urls))
]