from django.shortcuts import render

import requests
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiResponse , OpenApiParameter
from rest_framework import viewsets

from .models import *
from .serializers import  *
from base.models import *




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
   queryset = Place.objects.prefetch_related('images_place').select_related('place_type')  
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




import optuna
import pandas as pd



@extend_schema(
   description="Suggest a package based on the user's budget and preferred number of days. The API combines hotel and hauberge offers, optimizes the best package using Optuna, and returns the results sorted by the best budget and the corresponding stay duration.",
   parameters=[
      OpenApiParameter(name="min_budget", type=int, description="Minimum budget for the stay. Default is 50.", required=False),
      OpenApiParameter(name="max_budget", type=int, description="Maximum budget for the stay. Default is 500.", required=False),
      OpenApiParameter(name="min_days", type=int, description="Minimum number of days for the stay. Default is 1.", required=False),
      OpenApiParameter(name="max_days", type=int, description="Maximum number of days for the stay. Default is 10.", required=False),
   ],
   responses={
      200: OpenApiResponse(description="A successful response with recommended hotel and hauberge packages, including best budget and days."),
      400: OpenApiResponse(description="Bad request, incorrect query parameters."),
   }
)
class SuggestPackageView(APIView):
   def get(self, request):
      hotel_offres = HotelOffre.objects.filter(is_base=True).values("id", "name", "prix", "hotel__nom")
      hauberge_offres = HaubergeOffre.objects.all().values("id", "titre", "prix", "hauberge__nom")

      hotel_df = pd.DataFrame(list(hotel_offres))
      hauberge_df = pd.DataFrame(list(hauberge_offres))

      hotel_df.rename(columns={"hotel__nom": "location_name", "name": "offer_name", "prix": "price"}, inplace=True)
      hauberge_df.rename(columns={"hauberge__nom": "location_name", "titre": "offer_name", "prix": "price"}, inplace=True)

      hotel_df['type'] = 'hotel'
      hauberge_df['type'] = 'hauberge'

      combined_df = pd.concat([hotel_df, hauberge_df], ignore_index=True)
      combined_df = combined_df.dropna(subset=['price'])

      min_budget = int(request.query_params.get("min_budget", 50))
      max_budget = int(request.query_params.get("max_budget", 500))
      min_days = int(request.query_params.get("min_days", 1))
      max_days = int(request.query_params.get("max_days", 10))

      def objective(trial):
            budget = trial.suggest_int("budget", min_budget, max_budget)  
            days = trial.suggest_int("days", min_days, max_days)

            filtered_df = combined_df[combined_df['price'] <= budget]
            if filtered_df.empty:
               return float('inf')

            return min(filtered_df['price']) * days

      study = optuna.create_study(direction="minimize")
      study.optimize(objective, n_trials=20)

      
      best_budget = study.best_params['budget']
      best_days = study.best_params['days']
      final_offres = combined_df[combined_df['price'] <= best_budget]

      hotel_results = final_offres[final_offres['type'] == 'hotel'].to_dict(orient="records")
      hauberge_results = final_offres[final_offres['type'] == 'hauberge'].to_dict(orient="records")

      return Response({
            "best_budget": best_budget,
            "best_days": best_days,
            "hotels": hotel_results,
            "hauberges": hauberge_results
      })







@extend_schema(
    request = InputSer,  # Assuming InputSer is a serializer class for validating the input
    description="Gen AI Boumerdès - This API generates personalized travel recommendations for Boumerdès, Algeria based on user input. It leverages a Generative AI model to provide relevant suggestions, tips, and tourist attractions. You can specify the language (English, French, or Arabic) and provide input to tailor the recommendations to your preferences.",
    responses={
        200: OpenApiResponse(description="A successful response containing travel tips and recommendations based on the input provided."),
        400: OpenApiResponse(description="Bad request, input data or language is missing or invalid."),
        415: OpenApiResponse(description="Content-Type must be application/json."),
    }
)
@api_view(['POST'])
def gen_ai(request) : 
   
   if not request.content_type == 'application/json':
      return Response({"error": "Content-Type must be application/json."}, status=415)

   input_data = request.data["input_data"]
   if not input_data:
      return Response({"error": "Input field is required."}, status=400)

   language = request.data.get('language', 'en').lower()
   if language not in ['en', 'fr', 'ar']:
      return Response({"error": "Language must be 'en', 'fr', or 'ar'."}, status=400)

   try:
      # Call your external API (POST request)
      external_api_url = "https://khamedmohammedtaha.pythonanywhere.com/portfolio/api/boum/"
      payload = {"input": input_data, "language": language}
      headers = {"Content-Type": "application/json"}
      

      response = requests.post(external_api_url, json=payload, headers=headers)

      # Handle external API response
      if response.status_code == 200:
         data = response.json()
         
         return Response({"data": data}, status=200)
      else:
         return Response({"error": "External API call failed.", "details": response.text}, status=response.status_code)
   
   except requests.RequestException as e:
      return Response({"error": f"Request error: {str(e)}"}, status=500)