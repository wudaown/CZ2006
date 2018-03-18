# from django.contrib import admin
# from .models import Language, School, Level
#
#
# # Register your models here.
#
# class GlobalSetting(admin.AdminSite):
# 	site_title = 'Kindergarten Finder'
# 	site_header = 'Kindergarten Finder'
#
#
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
#
#
# admin_site = GlobalSetting(name="myadmin")
# admin_site.register(Language)
# admin_site.register(School, SchoolAdmin)
# admin_site.register(Level)
# admin.site.register(Language)
# admin.site.register(School, SchoolAdmin)
# admin.site.register(Level)

