from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("favorites/", views.FavoritesView.as_view(), name="favorites"),
    path("favorite/<int:pk>/", views.toggle_favorite, name="toggle_favorite"),
]
