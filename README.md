# CampusSwap (Group 10, COMP-8347)

A website where students can buy, sell, and give away used stuff.
Built with Django, Bootstrap 5 and SQLite.

Team: Karan Singh, Manpreet Kaur, Saloni Patel

## Quick start

```bash
python -m venv venv
venv\Scripts\activate            # Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata sample_data     # sample categories, listings, demo users
python manage.py runserver
```
Open http://127.0.0.1:8000/

Demo accounts (from the fixture), password for both is `campus123`:
- `demo_seller`
- `demo_buyer`

Admin: `python manage.py createsuperuser`, then open /admin/

Run the tests: `python manage.py test`

## Features (matches the proposal)

| Feature | Where |
|---|---|
| Browse listings (guests + students) | browse/ (HomeView) |
| Search by keyword + category dropdown | browse/views.py HomeView.get_queryset |
| Footer: About, Contact, Terms | templates/footer.html, browse/ |
| Sign up (campus email only), login, logout, forgot password | accounts/, templates/registration/ |
| Profile page | accounts/views.py ProfileView |
| Post / edit listings with photo upload | listings/ (ListingForm, Create/Update views) |
| Favorites | accounts/ (Favorite model, toggle_favorite) |
| Messages between users + inbox | browse/ (Message model) |
| Recently viewed (sessions) | listings/views.py ListingDetailView + HomeView |
| Models and fixtures | listings/models.py, listings/fixtures/sample_data.json |
| Class-based views + Bootstrap | all apps, templates/base.html |

## Who owns what

| Person | Files |
|---|---|
| Karan | project setup, base.html, listings/ app (models, fixtures, forms, create/edit/detail views, photo upload) |
| Manpreet | browse/ app: home grid, search + dropdown, recently viewed, messaging (model, form, inbox) |
| Saloni | accounts/ app: sign up, login, logout, password reset, profile, favorites; footer + About/Contact/Terms pages |

## Notes
- Sign-up only accepts emails ending with the domain in `CAMPUS_EMAIL_DOMAIN` (campusswap/settings.py, default `uwindsor.ca`). Change it to your campus domain.
- Password reset emails are printed in the terminal (console email backend). Copy the link from there.
- Uploaded photos are stored in `media/` (not committed to git).

## Git routine
```bash
git checkout -b your-name-feature
git add . && git commit -m "Describe what you did"
git push origin your-name-feature      # then open a Pull Request
git checkout main && git pull          # before starting new work
```
