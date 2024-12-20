from rest_framework import serializers
from .models import * 



class ResidentSerializer(serializers.ModelSerializer):
   first_name = serializers.CharField(write_only=True)
   last_name = serializers.CharField(write_only=True)
   email = serializers.EmailField( write_only=True)
   password = serializers.CharField(write_only=True)
   

   class Meta:
      model = Resident
      fields = ['first_name' ,'last_name' ,'email' , 'password']


class ResidentSerializerInfo(serializers.ModelSerializer):

   class Meta:
      model = Resident
      fields = "__all__"

class ResidentSerializerUpdate(serializers.ModelSerializer):

   class Meta:
      model = Resident
      fields = [ "date_naissance" , "lieu_naissance","sexe","numero_carte_identite"]


class LoginSerializer(serializers.ModelSerializer):
   email = serializers.EmailField( write_only=True)
   password = serializers.CharField(write_only=True)
   class Meta:
      model = User
      fields = ['email','password']