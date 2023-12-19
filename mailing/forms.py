from django import forms

from mailing.models import Mailing, Mail


class MailingForm(forms.ModelForm):
    """Форма добавления и редактирования рассылок"""
    class Meta:
        model = Mailing
        fields = ['name', 'send_date', 'repetitions',
                  'period', 'customers', 'mail', 'user']
        # Добавление классов к тегам для использования стилей CSS
        widgets = {
            'name': forms.TextInput(attrs={"class": "form-control my-2", "placeholder": "Название рассылки"}),
            'send_date': forms.SelectDateWidget(),
            # 'email': forms.EmailInput(attrs={"class": "form-control my-2", "placeholder": "e@mail.ru"}),
            # 'user': forms.Select(attrs={"class": "form-control my-2"}),
        }


class MailForm(forms.ModelForm):
    class Meta:
        model = Mail
        fields = ['title', 'body']


# MailingFormSet = forms.inlineformset_factory(parent_model=Mail,
#     model=Mailing, extra=1,
# )
