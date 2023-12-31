from django import forms
from django.core.exceptions import ValidationError
from customer.models import Customer


class StyleFormMixin:
    """Миксин для применения стилей к полям формы"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

            # if field.widget.input_type == 'text':
            #     field.widget.attrs['class'] = 'form-control'
            #     field.widget.attrs['placeholder'] = field.label
            # elif field.widget.input_type == 'email':
            #     field.widget.attrs['class'] = 'form-control'
            #     field.widget.attrs['placeholder'] = field.label
            # elif field.widget.input_type == 'password':
            #     field.widget.attrs['class'] = 'form-control'
            #     field.widget.attrs['placeholder'] = field.label
            # elif field.widget.input_type == 'select':
            #     field.widget.attrs['class'] = 'form-select'
            # elif field.widget.input_type == 'number':
            #     field.widget.attrs['class'] = 'form-control'
            # elif field.widget.input_type == 'file':
            #     field.widget.attrs['class'] = 'form-control'


class CustomerForm(StyleFormMixin, forms.ModelForm):
    """Форма добавления и редактирования клиентов"""
    def __init__(self, *args, **kwargs):
        """Передача user для проверки на уникальность email клиента текущего пользователя"""
        self.user = kwargs.pop('user')
        super(CustomerForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Customer
        fields = ['email', 'first_name', 'last_name']

    def clean(self):
        """Метод проверки уникальности email после валидации формы,
        если поле email было изменено"""
        cleaned_data = super().clean()
        if 'email' in self.changed_data:
            if Customer.objects.filter(user=self.user.pk, email=cleaned_data.get('email')).exists():
                raise ValidationError("Пользователь с таким e-mail уже существует")
        return cleaned_data
