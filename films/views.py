from django.shortcuts import render
from django.http import JsonResponse
from .models import Movie

# Create your views here.
def movie_list(request):
    movies = Movie.objects.all()
    data = {
        'movies':movies
    }
    return JsonResponse(data)

def movie_details(request, pk):
    movie = Movie.objects.get(pk=pk)
    print(movie.title)
    return JsonResponse(movie)