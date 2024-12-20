
from django.contrib import admin
from django.urls import  path , include

from drf_spectacular.views import SpectacularAPIView , SpectacularSwaggerView , SpectacularRedocView




urlpatterns = [
    path('dash/', admin.site.urls),
    path('base/' , include("base.urls") ) , 
    path('smart/' , include("Smart.urls")),


    # config api docs 
    path('api/swagger/schema/',SpectacularAPIView.as_view(),name="schema"),
    path('api/docs/',SpectacularSwaggerView.as_view(url_name="schema")),
    path('swagger/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
