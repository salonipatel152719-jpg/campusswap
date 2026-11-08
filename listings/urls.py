from django.urls import path
from . import views

urlpatterns = [
    path("new/", views.ListingCreateView.as_view(), name="listing_create"),
    path("<int:pk>/", views.ListingDetailView.as_view(), name="listing_detail"),
    path("<int:pk>/edit/", views.ListingUpdateView.as_view(), name="listing_update"),
]
