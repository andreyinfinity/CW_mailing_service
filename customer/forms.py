from django import forms
from django.core.exceptions import ValidationError

from customer.models import Customer


class CustomerForm(forms.ModelForm):
    """Форма добавления и редактирования клиентов"""
    def __init__(self, *args, **kwargs):
        """Передача user для проверки на уникальность email клиента текущего пользователя"""
        self.user = kwargs.pop('user')
        super(CustomerForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Customer
        fields = ['email', 'first_name', 'last_name']
        # Добавление классов к тегам для использования стилей CSS
        widgets = {
            'first_name': forms.TextInput(attrs={"class": "form-control my-2", "placeholder": "Имя"}),
            'last_name': forms.TextInput(attrs={"class": "form-control my-2", "placeholder": "Фамилия"}),
            'email': forms.EmailInput(attrs={"class": "form-control my-2", "placeholder": "e@mail.ru"}),
        }

    def clean(self):
        """Метод проверки уникальности email после валидации формы,
        если поле email было изменено"""
        cleaned_data = super().clean()
        if 'email' in self.changed_data:
            if Customer.objects.filter(user=self.user.pk, email=cleaned_data.get('email')).exists():
                raise ValidationError("Пользователь с таким e-mail уже существует")
        return cleaned_data
