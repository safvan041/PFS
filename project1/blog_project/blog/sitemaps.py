from django.contrib.sitemaps import Sitemap
from .models import Post
from django.urls import reverse

class PostSitemap(Sitemap):
    def items(self):
        return Post.objects.all()

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return reverse('post_detail', args=[obj.slug])
