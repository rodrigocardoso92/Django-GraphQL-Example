from django.contrib import admin

# Register your models here.
from post.models import Post, PostImage

class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 0

class ManagePost(admin.ModelAdmin):
    list_display = ('id', 'title', 'visualize', 'created_at', 'updated_at')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    list_editable = ('visualize',)
    list_per_page = 20
    inlines = [PostImageInline, ]

admin.site.register(Post, ManagePost)