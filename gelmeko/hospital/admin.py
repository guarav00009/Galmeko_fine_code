from django.contrib import admin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.utils.html import format_html
from hospital.models import HospitalUser
from django.urls import path
from django.conf.urls import include, url
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.utils.translation import gettext, gettext_lazy as _
from django.utils.translation import ugettext_lazy
from user.admin import admin_site

class HospitalUserAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = HospitalUser
    list_display = ('full_name','email', 'phone','address','status','Action')
    list_filter = ('status',)
    list_per_page = 5   #For Pagination

    fieldsets = (
        (None, {'fields': ('full_name','email','phone','address','status','password')}),
        ('Permissions', {'fields': ('is_active',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('full_name','email','phone','status','password', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('full_name',)

    def Action(self, obj):
        return format_html('<a class="user-detail" data-id =%s href="view/%s" title="View">%s</a>' % (obj.id,obj.id,'<i class="fa fa-eye" aria-hidden="true"></i>'))
    
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            url('^view/(?P<hospital_id>\d+)/$', self.hospital_view),
        ]
        return my_urls + urls

    def hospital_view(self, request,hospital_id):
        context = {
            'data' : HospitalUser.objects.all(),
            'available_apps' :  admin_site.get_app_list(request)
        }
        return TemplateResponse(request, 'admin/hospital_view.html', context=context)

admin_site.register(HospitalUser,HospitalUserAdmin)
