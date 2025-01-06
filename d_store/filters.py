from django import forms
from django_filters import FilterSet, ModelChoiceFilter, ChoiceFilter
from django.db.models import Q
from .models import Product, Category

class ProductFilter(FilterSet):
    brand = ChoiceFilter(
        choices=[(brand, brand) for brand in Product.objects.values_list('brand', flat=True).distinct() if brand],
        empty_label="Todas las marcas",
        label="Marcas",
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Product
        fields = ['brand']