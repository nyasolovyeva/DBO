from django.contrib import admin
from .models import Bank, DBOService


@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ['name', 'service_name', 'bank_type', 'branches_count', 'atms_count', 'years_existence']
    list_filter = ['bank_type']
    search_fields = ['name', 'service_name']
    list_per_page = 20
    actions = ['delete_all_banks']

    def delete_all_banks(self, request, queryset):
        count = Bank.objects.all().count()
        Bank.objects.all().delete()
        self.message_user(request, f'Удалено {count} банков')

    delete_all_banks.short_description = 'Удалить ВСЕ банки'


@admin.register(DBOService)
class DBOServiceAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'bank', 'ahp_rating',
        'monthly_fee_min', 'monthly_fee_max', 'mobile_app', 'two_factor_auth'
    ]
    list_filter = [
        'mobile_app', 'web_cabinet', 'two_factor_auth',
        'antifraud_automated', 'auto_tax_calculation', 'auto_tax_payment',
        'automatic_checks', 'cancel_checks', 'payment_by_phone', 'payment_by_qr',
        'payment_by_details', 'income_statistics', 'limit_control', 'support_online'
    ]
    search_fields = ['name', 'bank__name']
    list_per_page = 20
    actions = ['delete_all_services']

    def delete_all_services(self, request, queryset):
        count = DBOService.objects.all().count()
        DBOService.objects.all().delete()
        self.message_user(request, f'Удалено {count} сервисов')

    delete_all_services.short_description = 'Удалить ВСЕ сервисы'

    fieldsets = (
        ('Основная информация', {
            'fields': ('bank', 'name')
        }),
        ('Мобильное приложение и веб-кабинет', {
            'fields': ('mobile_app', 'web_cabinet')
        }),
        ('Скорость подключения', {
            'fields': ('onboarding_speed',)
        }),
        ('Налогово-учётная интеграция', {
            'fields': ('automatic_checks',  'cancel_checks', 'auto_tax_calculation', 'auto_tax_payment')
        }),
        ('Платёжно-расчётный функционал', {
            'fields': ('payment_by_phone', 'payment_by_qr', 'payment_by_details', 'sbp_integration')
        }),
        ('Дополнительные цифровые сервисы', {
            'fields': ('income_statistics', 'limit_control')
        }),
        ('Безопасность', {
            'fields': ('two_factor_auth', 'antifraud_automated', 'auto_logout', 'auto_logout_time')
        }),
        ('Международные переводы', {
            'fields': ('international_transfers', 'international_countries', 'swift_available')
        }),
        ('Стоимость', {
            'fields': ('monthly_fee_min', 'monthly_fee_max', 'free_conditions')
        }),
        ('Переводы', {
            'fields': ('internal_transfer_fee', 'sbp_transfer_fee', 'card_transfer_fee', 'transfer_free_limit')
        }),
        ('Снятие наличных', {
            'fields': ('cash_withdrawal_free_limit', 'cash_withdrawal_fee')
        }),
        ('Внесение наличных', {
            'fields': ('deposit_free_limit', 'deposit_fee')
        }),
        ('Поддержка', {
            'fields': ('support_online',)
        }),
    )

    def get_ahp_rating_display(self, obj):
        rating = obj.ahp_rating
        color = 'green' if rating >= 8 else 'orange' if rating >= 6 else 'red'
        return f'<span style="color: {color}; font-weight: bold;">{rating:.2f}</span>'

    get_ahp_rating_display.short_description = 'AHP рейтинг'
    get_ahp_rating_display.allow_tags = True