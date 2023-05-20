from django.urls import path, include
from .views import index, person, GenericPerson, PersonViewset, RegisterAPI, LoginAPI

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'people', PersonViewset)


urlpatterns = [
    path('index/', index),
    path('person/', person),
    path('generic/person/', GenericPerson.as_view()),
    path('generic/person/<int:id>', GenericPerson.as_view()),
    path('viewset/', include(router.urls)) ,
    path('register/', RegisterAPI.as_view()) ,
    path('login/', LoginAPI.as_view())
]

