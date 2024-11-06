from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = "daily"
    i18n = True

    def items(self):
        return ["index", "about-us", "find-us", "offers", "test-drive", "installment"]

    def location(self, item):
        return reverse(item)


# class CarSitemap(Sitemap):
#     changefreq = "weekly"
#     priority = 0.9
#     i18n = True
#
#     def items(self):
#         return Car.objects.all()
#
#     @staticmethod
#     def lastmod(obj):
#         return obj.updated_on
