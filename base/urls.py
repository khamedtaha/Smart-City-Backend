from django.urls import path
from . import views


urlpatterns = [
   path('' , views.test_main ) , 
   path('resident/signup' , views.create_resident , name ="create_resident") , 
   path('resident/login', views.custom_token_resident , name ="custom_token_resident"),
   path('resident/<str:pk>' , views.Resident_id.as_view() , name = "resident_info") ,

   #-----------------------------------------------------------------------------------
   path('hauberge/login' , views.custom_token_hauberge) , 
   path('hauberge/<str:pk_hauberge>/reservation' , views.get_Reservation_hauberge),
]
