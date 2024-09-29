from django.contrib import admin
from .models import public_user, Report, StaffUser, ReportMatch

@admin.register(public_user)
class PublicUserAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'verified', 'otp_created_at', 'created_at', 'last_login')  # Display these fields in the list view
    search_fields = ('phone_number',)  # Allow searching by phone number
    list_filter = ('verified', 'created_at', 'last_login')  # Allow filtering by verification status and creation date
    readonly_fields = ('created_at','last_login')  # Make 'created_at' field read-only

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('get_user_phone_number', 'report_type', 'status', 'last_seen_location', 'timestamp', 'report_id')  # Display these fields in the list view
    search_fields = ('user__phone_number', 'report_id', 'last_seen_location')  # Allow searching by user's phone number, report ID, and location
    list_filter = ('report_type', 'status', 'timestamp')  # Allow filtering by report type, status, and timestamp
    readonly_fields = ('timestamp', 'report_id')  # Make 'timestamp' and 'report_id' fields read-only

    def get_user_phone_number(self, obj):
        return obj.user.phone_number  # Display the related user's phone number in the admin list view
    get_user_phone_number.short_description = 'User Phone Number'  # Set the column name

@admin.register(ReportMatch)
class ReportMatchAdmin(admin.ModelAdmin):
    list_display = ('get_report_id', 'location', 'timestamp')  # Display these fields in the list view
    search_fields = ('report__report_id', 'location')  # Allow searching by report ID and location
    list_filter = ('location', 'timestamp')  # Allow filtering by location and timestamp
    readonly_fields = ('timestamp',)  # Make 'timestamp' field read-only

    def get_report_id(self, obj):
        return obj.report.report_id  # Display the related report's ID in the admin list view
    get_report_id.short_description = 'Report ID'  # Set the column name    

@admin.register(StaffUser)
class StaffUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'notification_preference', 'is_verified')
    search_fields = ('user__username', 'phone_number')
    list_filter = ('notification_preference', 'is_verified')
    ordering = ('user__username',)
    readonly_fields = ('user',)  # Make the user field readonly, as it's a OneToOne relationship
    