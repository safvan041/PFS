from django.contrib import admin
from .models import Post
from .models import Profile
from .models import Post, Category, Tag
from .models import Comment


admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Comment)