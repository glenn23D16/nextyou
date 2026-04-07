from django.urls import path
from .views import simulate

urlpatterns = [
    path('', simulate, name='simulate'),
]
