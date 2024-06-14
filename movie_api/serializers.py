from rest_framework import serializers
from .models import Movie, Review, UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"



class ReviewSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = "__all__"

class  MovieSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True,read_only=True)
    class Meta:
        model = Review
        fields = "__all__"