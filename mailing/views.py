from django.forms import inlineformset_factory
from django.urls import reverse_lazy
from django.views import generic

from mailing.forms import MailingForm, MailForm
from mailing.models import Mail, Mailing


class MailView(generic.ListView):
    model = Mail


class MailCreateView(generic.CreateView):
    model = Mail
    form_class = MailForm
    success_url = reverse_lazy('mailing:mails')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        MailingFormset = inlineformset_factory(Mail, Mailing, form=MailingForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = MailingFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = MailingFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


class MailUpdateView(generic.UpdateView):
    model = Mail
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mails')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        MailingFormset = inlineformset_factory(Mail, Mailing, form=MailingForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = MailingFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = MailingFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


class MailDeleteView(generic.DeleteView):
    model = Mail
    success_url = reverse_lazy('mailing:mails')

