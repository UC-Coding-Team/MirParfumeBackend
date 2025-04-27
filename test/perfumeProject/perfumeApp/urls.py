from django.urls import path
from .views import *

urlpatterns = [
    path('api/home/', HomeAPIView.as_view()),
    path('api/product/<slug:slug>/', ProductDetailAPIView.as_view())
]
