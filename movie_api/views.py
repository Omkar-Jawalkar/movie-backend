from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Movie, Review, UserProfile
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from .serializers import MovieSerializer,ReviewSerializer
from .filters import MovieFilter


class ReviewPagination(PageNumberPagination):
    page_size = 5  # Number of reviews per page



@api_view(['GET'])
def movie_list(request):
    filterset = MovieFilter(request.GET, queryset=Movie.objects.all())
    serializer = MovieSerializer(filterset.qs, many=True)
    pagination_class = None
    return Response({"data" : serializer.data, "error" : {}})

@api_view(['POST'])
def movie_create(request):
    serializer = MovieSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"data":serializer.data, "error" : {}}, status=status.HTTP_201_CREATED)
    return Response({"data" :{} , "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def movie_detail(request, pk):
    try:
        movie = Movie.objects.get(pk=pk)
    except Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = MovieSerializer(movie)
    return Response(serializer.data)

@api_view(['PUT'])
def movie_update(request, pk):
    try:
        movie = Movie.objects.get(pk=pk)
    except Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = MovieSerializer(movie, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"data":serializer.data, "error" : {}})
    return Response({"data" :{} , "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def movie_delete(request, pk):
    try:
        movie = Movie.objects.get(pk=pk)
    except Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    movie.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# review 

@api_view(['POST'])
def create_review(request, movie_id):
    try:
        movie = Movie.objects.get(pk=movie_id)
        user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
    except Movie.DoesNotExist:
        return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
    
    existing_review = Review.objects.filter(user=user_profile, movie=movie).first()
    if existing_review:
        return Response({'error': 'You have already reviewed this movie.'}, status=status.HTTP_400_BAD_REQUEST)


    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=user_profile, movie=movie)
        return Response({"data":serializer.data, "error" : {}}, status=status.HTTP_201_CREATED)
    return Response({"data" :{} , "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def list_reviews(request, movie_id):
    try:
        movie = Movie.objects.get(pk=movie_id)
    except Movie.DoesNotExist:
        return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)

    reviews = Review.objects.filter(movie=movie)
    paginator = ReviewPagination()
    paginated_reviews = paginator.paginate_queryset(reviews, request)
    serializer = ReviewSerializer(paginated_reviews, many=True)
    return paginator.get_paginated_response(serializer.data)


# Searching

@api_view(['GET'])
def search_movies(request):
    query = request.GET.get('q', '')
    movies = Movie.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    )
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)
