from django import forms
from django_filters import FilterSet, ModelChoiceFilter, ChoiceFilter
from django.db.models import Q
from .models import Product, Category


class ProductFilter(FilterSet):
    brand = ChoiceFilter(
        empty_label="Todas las marcas",
        label="Marcas",
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Product
        fields = ['brand']

    def __init__(self, *args, **kwargs):
        category = kwargs.pop('category', None)
        super().__init__(*args, **kwargs)

        if category:
            # Filtrar las opciones de marcas según los productos de la categoría
            self.filters['brand'].field.choices = [
                (brand, brand) for brand in category.products_parts.values_list('brand', flat=True).distinct() if brand
            ]