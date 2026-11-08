from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("inbox/", views.InboxView.as_view(), name="inbox"),
    path("message/<int:listing_pk>/", views.MessageCreateView.as_view(), name="message_create"),
    path("about/", views.StaticPage.as_view(template_name="browse/about.html"), name="about"),
    path("contact/", views.StaticPage.as_view(template_name="browse/contact.html"), name="contact"),
    path("terms/", views.StaticPage.as_view(template_name="browse/terms.html"), name="terms"),
]
