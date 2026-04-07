from django.urls import path

from . import views

urlpatterns = [
    path("health/", views.health, name="health"),
    path("contact/", views.contact_submit, name="contact_submit"),
]
