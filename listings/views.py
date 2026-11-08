from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DetailView

from .models import Listing
from .forms import ListingForm


class ListingCreateView(LoginRequiredMixin, CreateView):
    model = Listing
    form_class = ListingForm

    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)


class ListingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Listing
    form_class = ListingForm

    def test_func(self):
        return self.get_object().seller == self.request.user


class ListingDetailView(DetailView):
    model = Listing

    def get(self, request, *args, **kwargs):
        # Recently viewed items: keep the last 5 listing ids in the session
        recent = request.session.get("recent", [])
        pk = kwargs["pk"]
        if pk in recent:
            recent.remove(pk)
        recent.insert(0, pk)
        request.session["recent"] = recent[:5]
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        ctx["is_favorite"] = (
            user.is_authenticated
            and user.favorite_set.filter(listing=self.object).exists()
        )
        return ctx
