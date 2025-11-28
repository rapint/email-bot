from django.urls import path
from .views import home
from . import views

urlpatterns = [
    path("generate-message/", views.generate_message, name="generate_message"),
    path('', home, name='home'),
]

