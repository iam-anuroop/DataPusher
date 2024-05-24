from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import (
    AccountViewSet, 
    DestinationViewSet,
    AvailableDestinations,
    DataRecievingAPI
    )


router = DefaultRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'destinations', DestinationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('availabledestinations/', AvailableDestinations.as_view(), name='dest'),
    path('server/incoming_data/', DataRecievingAPI.as_view(), name='incoming-data')
]