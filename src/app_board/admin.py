from django.contrib import admin
from .models import Bb, Rubric, BbImage, Favorite


class BbAdmin (admin.ModelAdmin):
    list_display = ('rubric', 'title', 'content', 'price', 'published')
    list_display_links = ('title', 'content')
    search_fields = ('title', 'content')

admin.site.register(Bb, BbAdmin)
admin.site.register(Rubric)
admin.site.register(BbImage)
admin.site.register(Favorite)

