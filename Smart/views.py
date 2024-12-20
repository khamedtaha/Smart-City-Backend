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

   def get_serializer_context(self):
      context = super().get_serializer_context()
      context['request'] = self.request  # لإرجاع URL كامل للصور
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