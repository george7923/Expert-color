from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from core.sitemaps import PagesSitemap

urlpatterns = [
    path("admin/", admin.site.urls),
    path("sitemap.xml", sitemap, {"sitemaps": {"pages": PagesSitemap}}, name="django.contrib.sitemaps.views.sitemap"),
    path("", include("core.urls")),
]
