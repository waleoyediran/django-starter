from rest_framework import routers
from demoproject.api import views

api_router = routers.DefaultRouter()
api_router.register(r'users', views.UserViewSet)
