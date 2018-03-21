from .models import User, EmailVerifyRecord
from xadmin import views
import xadmin


class BaseSetting(object):
	enable_themes = True
	use_bootswatch = True


class GlobalSetting(object):
	site_title = 'Kindergarten Finder'
	site_footer = 'undefined'
	# To collapse the left columns
	menu_style = 'accordion'


# Register your models here.
class UserAdmin(object):
	pass


# unregister User when prompt already register
# to make sure all attributes are display
xadmin.site.unregister(User)
xadmin.site.register(User, UserAdmin)
xadmin.site.register(EmailVerifyRecord)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)
