from django.contrib import admin
from .models import Kindergarten, Language


# Register your models here.

class GlobalSetting(admin.AdminSite):
	site_title = 'Kindergarten Finder'
	site_header = 'Kindergarten Finder'


# class SchoolAdmin(admin.ModelAdmin):
# 	# To edit which are to attributes to be display in admin page
# 	list_display = ['centre_name', 'centre_code', 'vacancy']
# 	# attributes that enable for searching
# 	search_fields = ['centre_name', 'centre_code', 'vacancy']
# 	# attributes that enable for filter
# 	list_filter = ['centre_name', 'centre_code', 'vacancy']
#
# 	# fields: attributes that enable for edit
# 	# fields = ('centre_name', 'centre_code', 'vacancy')


class KindergartenAdmin(admin.ModelAdmin):
	list_display = ['name', 'postalcode']
	search_fields = ['name', 'postalcode']
	list_filter = ['type', 'bus', 'outdoor', 'language']
	filter_horizontal = ['language']


# admin_site = GlobalSetting(name="myadmin")
admin.site.register(Language)
# admin.site.register(School, SchoolAdmin)
admin.site.register(Kindergarten, KindergartenAdmin)

