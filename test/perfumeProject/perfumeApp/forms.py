from django import forms
from django_svg_image_form_field import SvgAndImageFormField
from .models import Category, SubCategory


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = []
        field_classes = {
            'icon': SvgAndImageFormField
        }


class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        exclude = []
        field_classes = {
            'icon': SvgAndImageFormField
        }
