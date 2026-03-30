from rest_framework import serializers
from .models import EmployeeProfile, EmployeeTermination


class EmployeeProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeProfile
        fields = '__all__'

class EmployeeTerminationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeTermination
        fields = '__all__'
