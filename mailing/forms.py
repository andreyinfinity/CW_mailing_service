from django import forms
from customer.forms import StyleFormMixin
from mailing.models import Mailing, Mail


class MailingForm(StyleFormMixin, forms.ModelForm):
    """Форма добавления и редактирования рассылок"""
    def __init__(self, *args, **kwargs):
        """Для выбора писем только текущего пользователя"""
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['mail'].queryset = Mail.objects.filter(user=user)

    class Meta:
        model = Mailing
        fields = ['name', 'send_date',
                  'period', 'mail']
        widgets = {'send_date': forms.DateInput(attrs={'type': 'date'})}


class MailForm(StyleFormMixin, forms.ModelForm):
    """Форма добавления и редактирования письма"""
    class Meta:
        model = Mail
        fields = ['title', 'body']
