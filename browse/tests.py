from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from accounts.models import Favorite
from browse.models import Message
from listings.models import Category, Listing


class CampusSwapSmokeTests(TestCase):
    def setUp(self):
        self.seller = User.objects.create_user("seller", "s@uwindsor.ca", "pass12345!")
        self.buyer = User.objects.create_user("buyer", "b@uwindsor.ca", "pass12345!")
        self.cat = Category.objects.create(name="Textbooks")
        self.other = Category.objects.create(name="Furniture")
        self.l1 = Listing.objects.create(seller=self.seller, title="Calculus Book",
                                         description="math", price=20, category=self.cat)
        self.l2 = Listing.objects.create(seller=self.seller, title="Desk",
                                         description="wood", price=0, category=self.other)

    def test_public_pages(self):
        for name in ["home", "about", "contact", "terms", "login", "signup", "password_reset"]:
            self.assertEqual(self.client.get(reverse(name)).status_code, 200, name)
        self.assertEqual(self.client.get(self.l1.get_absolute_url()).status_code, 200)

    def test_search_and_category(self):
        r = self.client.get(reverse("home"), {"q": "calculus"})
        self.assertContains(r, "Calculus Book")
        self.assertNotContains(r, "Desk</a>")
        r = self.client.get(reverse("home"), {"category": self.other.id})
        self.assertContains(r, "Desk")
        self.assertNotContains(r, "Calculus Book</a>")

    def test_login_required_pages_redirect(self):
        for name in ["listing_create", "inbox", "favorites", "profile"]:
            r = self.client.get(reverse(name))
            self.assertEqual(r.status_code, 302, name)

    def test_signup_requires_campus_email(self):
        bad = {"username": "x", "email": "x@gmail.com", "password1": "Strong#Pass99", "password2": "Strong#Pass99"}
        self.client.post(reverse("signup"), bad)
        self.assertFalse(User.objects.filter(username="x").exists())
        good = dict(bad, email="x@uwindsor.ca")
        self.client.post(reverse("signup"), good)
        self.assertTrue(User.objects.filter(username="x").exists())

    def test_post_listing_and_only_owner_can_edit(self):
        self.client.login(username="buyer", password="pass12345!")
        r = self.client.post(reverse("listing_create"), {
            "title": "Lamp", "description": "nice", "price": "5", "category": self.cat.id})
        self.assertEqual(r.status_code, 302)
        lamp = Listing.objects.get(title="Lamp")
        self.assertEqual(lamp.seller, self.buyer)
        # buyer cannot edit seller's listing
        r = self.client.get(reverse("listing_update", args=[self.l1.pk]))
        self.assertEqual(r.status_code, 403)
        # but can edit own
        r = self.client.get(reverse("listing_update", args=[lamp.pk]))
        self.assertEqual(r.status_code, 200)

    def test_favorites_toggle(self):
        self.client.login(username="buyer", password="pass12345!")
        self.client.post(reverse("toggle_favorite", args=[self.l1.pk]))
        self.assertEqual(Favorite.objects.count(), 1)
        self.assertContains(self.client.get(reverse("favorites")), "Calculus Book")
        self.client.post(reverse("toggle_favorite", args=[self.l1.pk]))
        self.assertEqual(Favorite.objects.count(), 0)

    def test_messaging(self):
        self.client.login(username="buyer", password="pass12345!")
        self.client.post(reverse("message_create", args=[self.l1.pk]), {"body": "Still available?"})
        m = Message.objects.get()
        self.assertEqual((m.sender, m.recipient, m.listing), (self.buyer, self.seller, self.l1))
        self.client.logout()
        self.client.login(username="seller", password="pass12345!")
        self.assertContains(self.client.get(reverse("inbox")), "Still available?")

    def test_recently_viewed_session(self):
        self.client.get(self.l1.get_absolute_url())
        self.client.get(self.l2.get_absolute_url())
        r = self.client.get(reverse("home"))
        self.assertContains(r, "Recently viewed")
        self.assertEqual(self.client.session["recent"], [self.l2.pk, self.l1.pk])

    def test_logout_and_login(self):
        self.assertTrue(self.client.login(username="buyer", password="pass12345!"))
        r = self.client.post(reverse("logout"))
        self.assertEqual(r.status_code, 302)
        r = self.client.post(reverse("login"), {"username": "buyer", "password": "pass12345!"})
        self.assertEqual(r.status_code, 302)
