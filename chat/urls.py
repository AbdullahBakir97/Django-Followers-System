from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChatRoomView, MessagesView

router = DefaultRouter()

urlpatterns = [
    path('rooms/', ChatRoomView.as_view(), name='chat_rooms'),
    path('messages/<str:roomId>/', MessagesView.as_view(), name='chat_messages'),
    path('', include(router.urls)),
]