from datetime import datetime

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from cinema.models import Movie, Cinema, Showtime
from cinema.serializers import (
    MovieSerializer,
    CinemaSerializer,
    ShowtimeSerializer,
)


class MovieList(generics.ListCreateAPIView):
    queryset = Movie.objects.filter(
        release_date__lte=datetime.now(), rental_over_date__gt=datetime.now()
    )
    serializer_class = MovieSerializer


class MovieDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class CinemaList(generics.ListCreateAPIView):
    queryset = Cinema.objects.all()
    serializer_class = CinemaSerializer


class CinemaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cinema.objects.all()
    serializer_class = CinemaSerializer


class ShowtimeList(generics.ListCreateAPIView):
    queryset = Showtime.objects.all()
    serializer_class = ShowtimeSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ["room__cinema", "movie", "start_time", "end_time"]


class ShowtimeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Showtime.objects.all()
    serializer_class = ShowtimeSerializer
