from django.core.cache import cache
from django.db.models import Q
from django.views import generic

from blog.models import Post
from config.settings import CACHE_ENABLED
from customer.models import Customer
from mailing.models import Mailing


class IndexView(generic.TemplateView):
    """Контроллер главной страницы"""
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        """Получение кверисетов с низкоуровневым кешированием"""
        context = super().get_context_data(**kwargs)
        if CACHE_ENABLED:
            total_mailings = cache.get_or_set(
                key='total_mailings',
                default=Mailing.objects.all().count(),
                timeout=60
            )
            active_mailings = cache.get_or_set(
                key='active_mailings',
                default=Mailing.objects.filter(Q(status='created') | Q(status='in progress')).count()
            )
            unique_customers = cache.get_or_set(
                key='unique_customers',
                default=Customer.objects.order_by('email').distinct('email').count()
            )
        else:
            total_mailings = Mailing.objects.all().count()
            active_mailings = Mailing.objects.filter(Q(status='created') | Q(status='in progress')).count()
            unique_customers = Customer.objects.order_by('email').distinct('email').count()
        context['total_mailings'] = total_mailings
        context['active_mailings'] = active_mailings
        context['unique_customers'] = unique_customers
        context['random_posts'] = Post.objects.order_by('?')[:3]
        return context
