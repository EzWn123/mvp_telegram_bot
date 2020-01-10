from django.urls import path
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'messages', views.MessageViewSet)

urlpatterns = [
    path('users/', views.UserListApiView.as_view()),
    path('users/<int:pk>', views.UserDetailApiView.as_view()),
]+router.urls
