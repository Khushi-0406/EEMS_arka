from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework import serializers

# ================= USER SERIALIZER =================
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)  # 🔥 HASHING HAPPENS HERE
        user.save()
        return user


# ================= EMAIL LOGIN SERIALIZER =================


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(
            request=self.context.get('request'),
            username=email,   # we mapped email as username
            password=password
        )

        if not user:
            raise serializers.ValidationError("Invalid email or password")

        data = super().get_token(user)

        return {
            "refresh": str(data),
            "access": str(data.access_token),
        }