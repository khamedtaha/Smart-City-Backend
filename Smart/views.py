from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiResponse


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
