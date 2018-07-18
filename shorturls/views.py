from django.shortcuts import redirect
from django.views.generic import DetailView
from django.views.generic.base import RedirectView
from django.views.generic.edit import CreateView

from .models import Link


class LinkForm(CreateView):
    model = Link
    fields = ['url']

    def form_valid(self, form):
        prev_link = Link.objects.filter(url=form.instance.url)
        if prev_link.exists():
            return redirect('show_link', pk=prev_link[0].id)
        return super(LinkForm, self).form_valid(form)


class LinkDetail(DetailView):
    model = Link


class RedirectToOriginalURL(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        short_url = kwargs['short_url']
        return Link.expand(short_url)
