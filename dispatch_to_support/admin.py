from django.contrib import admin
from dispatch_to_support.models import SupportTicket, Response


# Register your models here.
@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    '''
        Admin View for SupportTicket
    '''
    def sentiment(self, obj):
        return obj.feedback.metrics.sentiment

    def customer(self, obj):
        return obj.feedback.customer

    list_display = (
        'customer',
        'status',
        'sentiment',
        'opened',
        'closed',
        'support_person',
        'feedback',
    )
    list_filter = (
        'status',
        'opened',
        'closed',
    )
    # inlines = [
    #     Inline,
    # ]
    # raw_id_fields = ('',)
    # readonly_fields = ('',)
    # search_fields = ('',)


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    '''
        Admin View for Response
    '''
    # list_display = (
    #     # 'short_text',
    #     # 'support_ticket'
    #     # 'support_person',
    #     # 'date',
    #     )
    # list_filter = ('',)
    # inlines = [
    #     Inline,
    # ]
    # raw_id_fields = ('',)
    # readonly_fields = ('',)
    # search_fields = ('',)
