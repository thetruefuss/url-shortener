import random
import string

from django.test import TestCase
from django.urls import reverse

from .models import Link


class ShortenerTest(TestCase):
    def test_shortens(self):
        """
        Test that the url gets shorter.
        """
        url = 'http://www.example.com/'
        link = Link(url=url)
        short_url = Link.shorten(link)
        self.assertLess(len(short_url), len(url))

    def test_expands(self):
        """
        Test that expanded url is same as original url.
        """
        url = 'http://www.example.com/'
        link = Link(url=url)
        short_url = Link.shorten(link)
        link.save()
        expanded_url = Link.expand(short_url)
        self.assertEqual(len(expanded_url), len(url))

    def test_homepage(self):
        """
        Test that homepage exists and has form.
        """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)

    def test_shortener_form(self):
        """
        Test that submitting form returns a Link object.
        """
        url = 'http://www.example.com/'
        response = self.client.post(reverse('home'), {'url': url}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('link', response.context)
        link = response.context['link']
        short_url = Link.shorten(link)
        self.assertEqual(url, link.url)
        self.assertIn(short_url, str(response.content))

    def test_redirects_to_long_url(self):
        """
        Test that short URL redirects to long URL.
        """
        url = 'http://www.example.com/'
        link = Link.objects.create(url=url)
        short_url = Link.shorten(link)
        response = self.client.get(reverse('redirect_short_url', kwargs={'short_url': short_url}))
        self.assertRedirects(response, url, fetch_redirect_response=False)

    def test_recover_link_n_times(self):
        """
        Tests multiple times that after shortening and expanding, the original URL is recovered.
        """
        TIMES = 100
        for i in range(TIMES):
            uri = ''.join(random.sample(string.ascii_lowercase, 5))
            url = 'http://www.example.com/{}/{}'.format(i, uri)
            link = Link.objects.create(url=url)
            short_url = Link.shorten(link)
            long_url =  Link.expand(short_url)
            self.assertEqual(url, long_url)
