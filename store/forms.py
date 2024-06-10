from django import forms
from store.models import OrderItem, Order


class AddQuantityForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['quantity']


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone_number', 'city', 'post_office']

    def clean(self):
        cleaned_data = super().clean()
        for field_name, value in cleaned_data.items():
            if not value:
                raise forms.ValidationError(f"{field_name.capitalize()} is required")
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance


class ProductFilterForm(forms.Form):
    SORT_CHOICES = [
        ('name_asc', 'Ім\'я (A-Z)'),
        ('name_desc', 'Ім\'я (Z-A)'),
        ('price_asc', 'Ціна (За збільшенням)'),
        ('price_desc', 'Ціна (За зменшенням)'),
    ]

    sort_by = forms.ChoiceField(choices=SORT_CHOICES, required=False, label='Sort by')
