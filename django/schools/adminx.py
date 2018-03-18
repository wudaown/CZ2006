# from .models import Language, School, Level

from .models import School
import xadmin


class SchoolAdmin(object):
	# To edit which are to attributes to be display in admin page
	list_display = ['centre_name', 'centre_code', 'level']
	# attributes that enable for searching
	search_fields = ['centre_name', 'centre_code', 'level']
	# attributes that enable for filter
	list_filter = ['centre_name', 'centre_code', 'level', 'vacancy', 'language']
	# style_fields is important for m2m
	# https://github.com/sshwsfc/xadmin/blob/master/xadmin/plugins/multiselect.py
	# style_fields = ['level_offer', 'm2m_transfer']
	# fields: attributes that enable for edit
	# fields = ('centre_name', 'centre_code', 'vacancy')

class LevelAdmin(object):
	list_display = ['level', 'vacancy', 'kindergarten']
	search_fields = ['level', 'vacancy', 'kindergarten']
	list_filter = ['level', 'vacancy', 'kindergarten']
	style_fields = ['kindergarten', 'm2m_transfer']


xadmin.site.register(School, SchoolAdmin)
# xadmin.site.register(Language)
# xadmin.site.register(Level, LevelAdmin)
