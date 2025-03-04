from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiResponse
from django.contrib.auth.models import  Group
from rest_framework_simplejwt.tokens import RefreshToken
from .models import * 
from django.contrib.auth.models import User
from .serializers import  *
from django.db import transaction




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

#-------------------------------------------------------------------
@extend_schema(
   request=ResidentSerializer , 
   description="This is the Create Account Resident view.",
   responses={
      200: OpenApiResponse(
            description="A successful response",
      ),
      400: OpenApiResponse(
            description="Bad request. Possible duplicate username or other issues.",
      ),
   }
)
@api_view(['POST'])
def create_resident(request):
   try:
      email = request.data["email"]

      # Check if the email (username) already exists
      if User.objects.filter(username=email).exists():
            return Response(
               {"error": "A user with this email already exists."},
               status=400
            )

            # Create the User
      target_user = User.objects.create(
            username=email,
            first_name=request.data.get("first_name", ""),
            last_name=request.data.get("last_name", ""),
      )
      target_user.set_password(request.data["password"])
      target_user.save()

            # Create the Resident
      resident = Resident(
         user=target_user,
         nom=request.data['last_name'],
         prenom=request.data['first_name'],
         date_naissance=None
      )
      resident.save()

      # Add the user to the 'resident' group
      user_group = Group.objects.get(name='resident')
      target_user.groups.add(user_group)
      return Response({"msg": "Resident created successfully"})

   except Group.DoesNotExist:
      return Response({"error": "Group 'Resident' does not exist."}, status=400)
   except KeyError as e:
      return Response({"error": f"Missing field: {str(e)}"}, status=400)
   except Exception as e:
      return Response({"error": str(e)}, status=400)
   


@extend_schema(
   request = LoginSerializer ,
   description="This is the Login view for Resident .",
   responses={
      200: OpenApiResponse(
            description="A successful response",
      )
   }
)
@api_view(['POST'])
def custom_token_resident(request):
   email = request.data.get("email")
   password = request.data.get("password")

   # Check if the email and password are provided
   if not email or not password:
      return Response({"error": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

   try:
      user = User.objects.get(username=email)
      id_resident = Resident.objects.get(user = user)
      if user.check_password(password):
            if user.groups.filter(name='resident').exists():
               refresh = RefreshToken.for_user(user)
               return Response({
                  "refresh": str(refresh),
                  "access": str(refresh.access_token) ,
                  "id_user" : user.id,
                  "id_resident" : id_resident.id
               }, status=status.HTTP_200_OK)
            else:
               return Response({"error": "User is not in the Customer group."}, status=status.HTTP_403_FORBIDDEN)
      else:
         return Response({"error": "Invalid password."}, status=status.HTTP_401_UNAUTHORIZED)

   except User.DoesNotExist:
      return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)



@extend_schema(
   request = ResidentSerializerUpdate ,
   description="This is  get info  or updating resident information .",
   responses={
      200: OpenApiResponse(
            description="A successful response",
      )
   }
)
class Resident_id(APIView) : 
   
   def get(self , request , pk ) : 
      try : 
         resident = Resident.objects.get( pk = pk ) 
      except Resident.DoesNotExist : 
         return Response({"msg" : "error exists !"},status=status.HTTP_404_NOT_FOUND)
      
      serializer = ResidentSerializerInfo( resident , many = False)
      return Response(serializer.data , status = status.HTTP_200_OK )
   
   def put(self , request , pk ) : 
         try : 
            resident = Resident.objects.get( pk = pk ) 
         except Resident.DoesNotExist : 
            return Response({"msg" : "error exists !"},status=status.HTTP_404_NOT_FOUND)
         
         serializer = ResidentSerializerInfo( resident ,  data = request.data )
         if serializer.is_valid(): 
            serializer.save()
            return Response({"msg" : "The process of updating resident information has been successfully completed"} , status=status.HTTP_201_CREATED)
         else : 
            return Response({"msg" : "The process of updating resident information has not been successfully completed"} , status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
   request = LoginSerializer ,
   description="This is the Login view for hauberge .",
   responses={
      200: OpenApiResponse(
            description="A successful response",
      )
   }
)
@api_view(['POST'])
def custom_token_hauberge(request):
   email = request.data.get("email")
   password = request.data.get("password")

   # Check if the email and password are provided
   if not email or not password:
      return Response({"error": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

   try:
      user = User.objects.get(username=email)
      id_hauberge = Hauberge.objects.get(user = user)
      if user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                  "refresh": str(refresh),
                  "access": str(refresh.access_token) ,
                  "id_user" : user.id,
                  "id_resident" : id_hauberge.id
            }, status=status.HTTP_200_OK)

      else:
         return Response({"error": "Invalid password."}, status=status.HTTP_401_UNAUTHORIZED)

   except User.DoesNotExist:
      return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)




@extend_schema(
   request = ReservationSer ,
   description="This is the get Reservation par id  hauberge .",
   responses={
      200: OpenApiResponse(
            description="A successful response",
      )
   }
)
@api_view(['GET'])
def get_Reservation_hauberge(request , pk_hauberge) : 
   try  : 
      reservations =  Reservation.objects.filter(hauberge = pk_hauberge )
      ser  =  ReservationSer( reservations  , many  = True)
      return Response(ser.data , status=status.HTTP_200_OK)
   except : 
      Response({"msg" : "error exists"} , status=status.HTTP_400_BAD_REQUEST)





@extend_schema(
   description="Verify if a person with the given ID card number is present in the blacklist",

   responses={
      200: OpenApiResponse(description="A successful response indicating whether the person is in the blacklist or not."),
      400: OpenApiResponse(description="Bad request, invalid ID card number."),
   }
)
@api_view(['GET'])
def verify_in_blaklist(request , id_card) : 
   if BlackList.objects.filter(numero_carte_identite = id_card).exists() : 
      return Response({"msg" : "This person is in the blacklist, handle with care ."})
   else : 
      return Response({"msg" : "This person is not in the blacklist ."})
   



@extend_schema(
   description="Create a new reservation for a specific Hauberge.",
   request=ReservationSer,
   responses={
      201: OpenApiResponse(description="A successful response with the created reservation."),
      400: OpenApiResponse(description="Bad request, invalid data or error.")
   }
)
@api_view(['POST'])
def create_reservation_hauberge(request, pk_hauberge):

   try:
      # Add the Hauberge foreign key to the reservation data
      data = request.data.copy()
      data['hauberge'] = pk_hauberge  # Automatically associate with the Hauberge by pk_hauberge
   
      # Serialize the data and validate it
      ser = ReservationSer(data=data)
      if ser.is_valid():
         # Save the new reservation
         ser.save()
         return Response(ser.data, status=status.HTTP_201_CREATED)
      else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
   except Exception as e:
      return Response({"msg": f"Error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)