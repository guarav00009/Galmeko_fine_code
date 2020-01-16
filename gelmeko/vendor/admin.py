from django.contrib import admin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.utils.html import format_html
from vendor.models import VendorUser
from django.urls import path
from django.conf.urls import include, url
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.utils.translation import gettext, gettext_lazy as _
from django.utils.translation import ugettext_lazy
from user.admin import admin_site


class VendorUserAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = VendorUser
    list_display = ('full_name','email','company_name','phone','status','Action')
    list_filter = ('status',)
    list_per_page = 5   #For Pagination
    fieldsets = (
        (None, {'fields': ('full_name','email','company_name','phone','password','status')}),
        ('Permissions', {'fields': ('is_active',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('full_name','email','company_name', 'phone','password', 'is_active','status')}
        ),
    )
    search_fields = ('email','full_name')
    ordering = ('full_name',)

    
    def Action(self, obj):
        return format_html('<a class="user-detail" data-id =%s href="view/%s" title="View">%s</a>' % (obj.id,obj.id,'<i class="fa fa-eye" aria-hidden="true"></i>'))
    
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            url('^view/(?P<vendor_id>\d+)/$', self.vendor_view),
        ]
        return my_urls + urls

    def vendor_view(self, request,vendor_id):
        context = {
            'data' : VendorUser.objects.all(),
            'available_apps' :  admin_site.get_app_list(request)
        }
        return TemplateResponse(request, 'admin/vendor_view.html', context=context)

admin_site.register(VendorUser,VendorUserAdmin)