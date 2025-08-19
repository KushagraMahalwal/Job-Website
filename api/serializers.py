from rest_framework import serializers
from api.models import job, User
from django.contrib.auth.hashers import make_password

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "role"]

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return User.objects.create(**validated_data)


class JobSerializer(serializers.ModelSerializer):
    posted_by = serializers.CharField(source="posted_by.username", read_only=True, allow_null=True)
    apply_by = serializers.SlugRelatedField(
            many=True,
            read_only=True,
            slug_field='username'
        )    
    class Meta:
        model = job   # your job model
        fields = ["id", "title", "description", "posted_by", "apply_by"]
    
