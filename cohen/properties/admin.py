# coding:utf-8

from django.contrib import admin
from django.utils.html import format_html

from .models import Property

admin.site.disable_action('delete_selected')


class PropertyAdmin(admin.ModelAdmin):
    list_fields = ('address', 'preview',)
    list_display = ('address', 'preview',)

    def preview(self, obj):
        tag = '<img src="{}" width="150" height="150" />'.format(obj.image.url)
        return tag

    preview.allow_tags = True
    preview.short_description = 'preview'

    def get_readonly_fields(self, request, obj=None):
        fields = [f.name for f in self.model._meta.fields]

        index = fields.index('image')
        fields.insert(index + 1, 'preview')

        return fields

    def has_add_permission(self, request):
        return False

    def change_view(self, request, object_id, extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save'] = False
        return super(PropertyAdmin, self).change_view(
            request, object_id, extra_context=extra_context)

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Property, PropertyAdmin)
