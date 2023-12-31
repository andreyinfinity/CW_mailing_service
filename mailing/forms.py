from django import forms

from mailing.models import Mailing, Mail


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class MailingForm(StyleFormMixin, forms.ModelForm):
    """Форма добавления и редактирования рассылок"""
    class Meta:
        model = Mailing
        fields = ['name', 'send_date', 'repetitions',
                  'period', 'mail']
        widgets = {'send_date': forms.DateTimeInput(attrs={'type': 'datetime-local'})}


class MailForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Mail
        fields = ['title', 'body']
