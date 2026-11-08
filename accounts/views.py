from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, ListView, TemplateView

from listings.models import Listing
from .forms import SignUpForm
from .models import Favorite


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["my_listings"] = Listing.objects.filter(seller=self.request.user)
        return ctx


@login_required
@require_POST
def toggle_favorite(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    fav, created = Favorite.objects.get_or_create(user=request.user, listing=listing)
    if not created:
        fav.delete()
    return redirect("listing_detail", pk=pk)


class FavoritesView(LoginRequiredMixin, ListView):
    template_name = "accounts/favorites.html"
    context_object_name = "favorites"

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).select_related("listing")
