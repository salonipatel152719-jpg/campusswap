from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView

from listings.models import Listing, Category
from .models import Message


class HomeView(ListView):
    """Home page: photo grid + keyword search + category dropdown + recently viewed."""
    model = Listing
    template_name = "browse/home.html"
    context_object_name = "listings"
    ordering = ["-created_at"]

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get("q", "").strip()
        cat = self.request.GET.get("category", "")
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
        if cat.isdigit():
            qs = qs.filter(category_id=cat)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["categories"] = Category.objects.all()
        ctx["q"] = self.request.GET.get("q", "")
        ctx["selected_category"] = self.request.GET.get("category", "")
        # Recently viewed (stored in the session by ListingDetailView)
        ids = self.request.session.get("recent", [])
        found = {l.pk: l for l in Listing.objects.filter(pk__in=ids)}
        ctx["recent"] = [found[i] for i in ids if i in found]
        return ctx


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["body"]
        labels = {"body": "Your message"}
        widgets = {"body": forms.Textarea(attrs={"rows": 4, "class": "form-control"})}


class MessageCreateView(LoginRequiredMixin, CreateView):
    form_class = MessageForm
    template_name = "browse/message_form.html"
    success_url = reverse_lazy("inbox")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["listing"] = get_object_or_404(Listing, pk=self.kwargs["listing_pk"])
        return ctx

    def form_valid(self, form):
        listing = get_object_or_404(Listing, pk=self.kwargs["listing_pk"])
        form.instance.sender = self.request.user
        form.instance.recipient = listing.seller
        form.instance.listing = listing
        return super().form_valid(form)


class InboxView(LoginRequiredMixin, ListView):
    template_name = "browse/inbox.html"
    context_object_name = "messages_received"

    def get_queryset(self):
        return (
            Message.objects.filter(recipient=self.request.user)
            .select_related("sender", "listing")
            .order_by("-created_at")
        )


class StaticPage(TemplateView):
    """About / Contact / Terms pages (footer links)."""
