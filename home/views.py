from django.db.models import Q
from django.shortcuts import render
from django.views import generic

from blog.models import Post
from customer.models import Customer
from mailing.models import Mailing


class IndexView(generic.TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_mailings'] = Mailing.objects.all().count()
        context['active_mailings'] = Mailing.objects.filter(Q(status='created') | Q(status='in progress')).count()
        context['unique_customers'] = Customer.objects.order_by('email').distinct('email').count()
        context['random_posts'] = Post.objects.order_by('?')[:3]
        return context
