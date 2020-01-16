from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from vendor.models import VendorUser
from hospital.models import HospitalUser
from vehicle.models import Vehicle
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.utils.html import format_html
from django.contrib.auth.models import Group
from .models import User
from django.urls import path
from django.conf.urls import include, url
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.utils.translation import gettext, gettext_lazy as _
from django.utils.translation import ugettext_lazy

class MyAdminSite(admin.AdminSite):
    index_title = ugettext_lazy('admin')

    def each_context(self, request):
        """
        Return a dictionary of variables to put in the template context for
        *every* page in the admin site.

        For sites running on a subpath, use the SCRIPT_NAME value if site_url
        hasn't been customized.
        """
        self.site_title = ugettext_lazy('Vendor')
        self.index_title = ugettext_lazy('Dashboard')
        self.site_header = ugettext_lazy('GLEMKO')
        
        script_name = request.META['SCRIPT_NAME']
        site_url = script_name if self.site_url == '/' and script_name else self.site_url
        return {
            'site_title': self.site_title,
            'site_header': self.site_header,
            'site_url': site_url,
            'has_permission': self.has_permission(request),
            'available_apps': self.get_app_list(request),
            'is_popup': False,
        }

admin_site = MyAdminSite()


class UserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('full_name','email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    list_per_page = 10 # No of records per page 
    fieldsets = (
        (None, {'fields': ('full_name','email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('full_name','email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

# class VendorUserAdmin(admin.ModelAdmin):
#     add_form = CustomUserCreationForm
#     form = CustomUserChangeForm
#     model = VendorUser
#     list_display = ('full_name','email','company_name','phone','status','Action')
#     list_filter = ('status',)
#     list_per_page = 5   
#     fieldsets = (
#         (None, {'fields': ('full_name','email','company_name','phone','password','status')}),
#         ('Permissions', {'fields': ('is_active',)}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('full_name','email','company_name', 'phone','password', 'is_active','status')}
#         ),
#     )
#     search_fields = ('email','full_name')
#     ordering = ('full_name',)


#     def Action(self, obj):
#         return format_html('<a class="user-detail" data-id =%s href="view/%s" title="View">%s</a>' % (obj.id,obj.id,'<i class="fa fa-eye" aria-hidden="true"></i>'))
    
#     def get_urls(self):
#         urls = super().get_urls()
#         my_urls = [
#             url('^view/(?P<vendor_id>\d+)/$', self.vendor_view),
#         ]
#         return my_urls + urls

#     def vendor_view(self, request,vendor_id):
#         context = {
#             'data' : VendorUser.objects.all(),
#             'available_apps' :  admin_site.get_app_list(request)
#         }
#         return TemplateResponse(request, 'admin/vendor_view.html', context=context)


admin_site.register(Vehicle)
admin_site.register(User, UserAdmin)
