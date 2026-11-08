from django import forms
from .models import Listing


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "description", "price", "category", "image"]
        widgets = {"description": forms.Textarea(attrs={"rows": 4})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            css = "form-select" if name == "category" else "form-control"
            field.widget.attrs["class"] = css
