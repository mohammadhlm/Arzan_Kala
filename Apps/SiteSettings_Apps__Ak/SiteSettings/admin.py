from django.contrib import admin
# Site Settings Model
from .models import SiteSettings
# Brand Photo (Relational Site Settins) Model
from .models import BrandPhotoModel

# Select SiteSetting Model
from .models import SelectSiteSetting

# Register your models here.
# Site Settings Admin
admin.site.register(SiteSettings)
# Brand Photo (Site Settings) Admin
admin.site.register(BrandPhotoModel)
# Select SiteSetting Admin
admin.site.register(SelectSiteSetting)
