from django.urls import path , include
from . import views
from rest_framework.routers import DefaultRouter
from .views import HotelViewSet , PlaceViewSet , SuggestPackageView




router = DefaultRouter()
router.register(r'hotels', HotelViewSet, basename='hotel')
router.register(r'places', PlaceViewSet, basename='place')

urlpatterns = [
   path('', include(router.urls)) , 
   path('place/types' , views.list_place_type) , 
   path('suggest-package/', SuggestPackageView.as_view(), name='suggest-package'),
   path('genai' , views.gen_ai) , 
]