from django.contrib import admin
from django.urls import path

from shorturls import views

urlpatterns = [
    path('', views.LinkForm.as_view(), name='home'),
    path('link/<int:pk>', views.LinkDetail.as_view(), name='show_link'),
    path('r/<slug:short_url>', views.RedirectToOriginalURL.as_view(), name='redirect_short_url'),

    path('admin/', admin.site.urls),
]
