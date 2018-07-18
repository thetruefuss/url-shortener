from django.db import models
from django.urls import reverse
from django.utils import timezone

from .utils import base_n_to_decimal, decimal_to_base_n


class Link(models.Model):
    url = models.URLField()
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('-created',)

    def get_absolute_url(self):
        return reverse('show_link', kwargs={'pk': self.pk})

    def short_url(self):
        return reverse('redirect_short_url', kwargs={'short_url': Link.shorten(self)})

    @staticmethod
    def shorten(link):
        link, _ = Link.objects.get_or_create(url=link.url)
        return str(decimal_to_base_n(link.id))

    @staticmethod
    def expand(slug):
        link_id = int(base_n_to_decimal(slug))
        link = Link.objects.get(id=link_id)
        return link.url
