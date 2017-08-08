from django import forms
from .models import Product
PUBLISH_CHOICES = (
    ("pubish","Publish"),
    ("draft","Draft"),
)
class ProductAddForm(forms.Form):
    title = forms.CharField(label="Your Title", widget=forms.TextInput(
        attrs = {
            "class": "custom-class",
            "placeholder": "Enter Your Title Here",
        }
    ))
    description = forms.CharField(widget = forms.Textarea(
        attrs = {
            "class": "my-custom-class",
            "placeholder": "Enter Your Description Here",
            "custom-attribute": "madeUp-attribute",
        }
    )) # This might cause an error...we'll see
    price = forms.DecimalField()
    publish = forms.ChoiceField(widget = forms.RadioSelect, choices = PUBLISH_CHOICES, required=False)


    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price <= 1.00:
            raise forms.ValidationError("Price must be greater than $1.00")
        elif price >= 99.99:
            raise forms.ValidationError("Price must be less than $100.00")
        else:
            return price
    def clean_title(self):
        title = self.cleaned_data.get("title")
        if len(title) > 3:
            return title
        else:
            raise forms.ValidationError("Title must be greater than 3 characters long.")
