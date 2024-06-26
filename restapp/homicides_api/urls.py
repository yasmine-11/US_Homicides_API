from django.urls import include, path
from rest_framework.routers import DefaultRouter
from homicides_api.views import index
from homicides_api.views import *

router = DefaultRouter()
router.register(r'victims', VictimViewSet)
router.register(r'locations', LocationViewSet)
router.register(r'dispositions', DispositionViewSet)
router.register(r'homicides', HomicideViewSet)

urlpatterns = [
    path('', index, name='index'),
    path('', include(router.urls)),
]
