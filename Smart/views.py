from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import viewsets

from .models import *
from .serializers import  *





@extend_schema(
   description="This is the Test config of app ",
   responses={
      200: OpenApiResponse(
            description="A successful response",
      )
   }
)
@api_view(["GET"])
def test_main(request) : 
   return Response({"msg" : "Test done"} , status=status.HTTP_200_OK)


@extend_schema(
   description="This endpoint retrieves a list of hotels along with their images.",
   responses={
      200: OpenApiResponse(description="A successful response with a list of hotels."),
   }
)
class HotelViewSet(viewsets.ModelViewSet):
   queryset = Hotel.objects.all()
   serializer_class = HotelSerializer
   
   def get_queryset(self) :
      return Hotel.objects.all().prefetch_related(
         'images_hotel',         # Prefetch related images
         'hotel_offre'           # Prefetch related offers
      )
   def get_serializer_context(self):
      context = super().get_serializer_context()
      context['request'] = self.request  
      return context


@extend_schema(
   description="This endpoint retrieves a list of Places along with their images.",
   responses={
      200: OpenApiResponse(description="A successful response with a list of hotels."),
   }
)
class PlaceViewSet(viewsets.ModelViewSet):
   queryset = Place.objects.prefetch_related('images_place').select_related('place_type')  # تحسين الأداء
   serializer_class = PlaceSerializer


@extend_schema(
   description="This endpoint retrieves a list of PlacesType ",
   responses={
      200: OpenApiResponse(description="A successful response with a list of hotels."),
   }
)
@api_view(["GET"])
def list_place_type(request) : 
   all_place_type  = PlaceType.objects.all()
   ser = PlaceTypeSerializer(all_place_type , many = True)
   return Response(ser.data , status=status.HTTP_200_OK)