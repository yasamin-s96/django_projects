from django.urls import path
from . import views
from .views import ActiveListingsView

urlpatterns = [
    path("", ActiveListingsView.as_view(), name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("create_listing/", views.create_listing, name="create listing"),
    path("listing/<int:listing_id>/", views.listing_details, name="listing details"),
]
