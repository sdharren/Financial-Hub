from rest_framework.serializers import ModelSerializer
from assetManager.models import User

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email", "first_name", "last_name", "password"
        ]

    def create(self, validated_data):
        user = User.objects.create_user(
            email = validated_data["email"],
            first_name = validated_data["first_name"],
            last_name = validated_data["last_name"],
            password = validated_data["password"]
        )

        return user