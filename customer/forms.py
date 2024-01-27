from django import forms
from customer.models import Customer


class StyleFormMixin:
    """Миксин для применения стилей к полям формы"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class CustomerForm(StyleFormMixin, forms.ModelForm):
    """Форма добавления и редактирования клиентов"""
    class Meta:
        model = Customer
        fields = ['email', 'first_name', 'last_name']
