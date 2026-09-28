from django.contrib import admin

# Register your models here.
from .models import ThreatLog

@admin.register(ThreatLog)
class ThreatLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'timestamp', 'proto', 'service', 'state', 'prediction', 'threat_level')
    list_filter = ('prediction', 'threat_level', 'proto')
    ordering = ('-timestamp',)

admin.site.site_header = "Telecom Threat Admin"
admin.site.site_url = "/dashboard/"  # makes "View site" link go to your dashboard instead of "/"