from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Movie, Review, UserProfile
from .serializers import MovieSerializer,ReviewSerializer

@api_view(['GET'])
def movie_list(request):
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)
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
    serializer = ReviewSerializer(reviews, many=True)
    return Response({"data" : serializer.data, "error" : {}})
