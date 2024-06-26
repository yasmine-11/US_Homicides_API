from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from homicides_api.models import *
from homicides_api.serializers import *
from django.utils.dateparse import parse_date
from django.db.models import Count
from rest_framework.pagination import PageNumberPagination


def index(request):
    return render(request, 'index.html')

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class VictimViewSet(viewsets.ModelViewSet):
    queryset = Victim.objects.all()
    serializer_class = VictimSerializer
    pagination_class = StandardResultsSetPagination

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    pagination_class = StandardResultsSetPagination

class DispositionViewSet(viewsets.ModelViewSet):
    queryset = Disposition.objects.all()
    serializer_class = DispositionSerializer
    pagination_class = StandardResultsSetPagination

class HomicideViewSet(viewsets.ModelViewSet):
    queryset = Homicide.objects.all().order_by('id')
    serializer_class = HomicideSerializer

    # ENDPOINT 1
    # GET: homicides by race
    @action(detail=False, methods=['get'], url_path='by-victim-race')
    def get_by_victim_race(self, request):
        race = request.query_params.get('race')
        if race:
            homicides = self.queryset.filter(victim__race=race)
            page = self.paginate_queryset(homicides)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(homicides, many=True)
            return Response(serializer.data)
        return Response({"error": "Race query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    # ENDPOINT 2
    # GET: Homicides by Victim Gender and Age Range
    @action(detail=False, methods=['get'], url_path='by-gender-age-range')
    def get_by_gender_age_range(self, request):
        gender = request.query_params.get('gender')
        min_age = request.query_params.get('min_age')
        max_age = request.query_params.get('max_age')
        if gender and min_age and max_age:
            homicides = self.queryset.filter(victim__sex=gender, victim__age__gte=min_age, victim__age__lte=max_age)
            page = self.paginate_queryset(homicides)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(homicides, many=True)
            return Response(serializer.data)
        return Response({"error": "Gender, min_age, and max_age query parameters are required"}, status=status.HTTP_400_BAD_REQUEST)

    # ENDPOINT 3
    # GET: Homicides Count by City
    @action(detail=False, methods=['get'], url_path='homicides-count-by-city')
    def get_homicides_count_by_city(self, request):
        homicides_count = self.queryset.values('location__city').annotate(count=Count('id'))
        return Response(homicides_count)

    # ENDPOINT 4
    # POST: Add a new homicide record
    def create(self, request, *args, **kwargs):
        victim_data = request.data.pop('victim')
        location_data = request.data.pop('location')
        disposition_data = request.data.pop('disposition')

        victim = Victim.objects.create(**victim_data)
        location = Location.objects.create(**location_data)
        disposition = Disposition.objects.create(**disposition_data)

        homicide = Homicide.objects.create(victim=victim, location=location, disposition=disposition, **request.data)
        serializer = self.get_serializer(homicide)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # ENDPOINT 5
    # PUT: Update a homicide's details
    def update(self, request, *args, **kwargs):
        # Supports partial updates if partial=True
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        victim_data = request.data.pop('victim', None)
        location_data = request.data.pop('location', None)
        disposition_data = request.data.pop('disposition', None)

        if victim_data:
            for attr, value in victim_data.items():
                setattr(instance.victim, attr, value)
            instance.victim.save()

        if location_data:
            for attr, value in location_data.items():
                setattr(instance.location, attr, value)
            instance.location.save()

        if disposition_data:
            for attr, value in disposition_data.items():
                setattr(instance.disposition, attr, value)
            instance.disposition.save()

        for attr, value in request.data.items():
            setattr(instance, attr, value)
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    # ENDPOINT 6
    # DELETE: Delete a homicide record
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

