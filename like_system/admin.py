from django.contrib import admin
from like_system.models import Like


class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_type', 'object_pk', )
    list_filter = ('content_type', )
    raw_id_fields = ('user', )

admin.site.register(Like, LikeAdmin)
