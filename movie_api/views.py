from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Movie
from .serializers import MovieSerializer

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