from django.core.management.base import BaseCommand
from services.models import Bank, DBOService

class Command(BaseCommand):
    help = 'Добавляет данные банков из таблицы'

    def handle(self, *args, **kwargs):
        # Очистка
        DBOService.objects.all().delete()
        Bank.objects.all().delete()

        # Данные банков
        banks_data = [
            {
                'name': 'Сбербанк',
                'service_name': 'Своё дело',
                'bank_type': 'state',
                'license_number': '1481', #
                'founded_year': 1841, #
                'years_existence': 185, #
                'branches_count': 39, #
                'atms_count': 214, #
                'financial_rating': 1, #
                'public_rating': 20, #
                'avg_customer_rating': 2.21, #
                'phone': '8-800-555-55-50', #
                'website': 'https://www.sberbank.ru', #
                'support_online': True, #
                'description': 'Крупнейший банк России с государственным участием',
            },
            {
                'name': 'Т-Банк',
                'service_name': 'Самозанятость',
                'bank_type': 'private',
                'license_number': '2673', #
                'founded_year': 2006, #
                'years_existence': 20, #
                'branches_count': 0,
                'atms_count': 125, #
                'financial_rating': 8, #
                'public_rating': 6, #
                'avg_customer_rating': 3.97, #
                'phone': '8-800-555-77-78', #
                'website': 'https://www.tbank.ru', #
                'support_online': True, #
                'description': 'Первый российский банк без отделений',
            },
            {
                'name': 'Альфа-Банк',
                'service_name': 'Самозанятые',
                'bank_type': 'private',
                'license_number': '1326', #
                'founded_year': 1990, #
                'years_existence': 36, #
                'branches_count': 9, #
                'atms_count': 51, #
                'financial_rating': 4, #
                'public_rating': 2, #
                'avg_customer_rating': 4.76, #
                'phone': '8-800-200-00-00', #
                'website': 'https://alfabank.ru', #
                'support_online': True, #
                'description': 'Крупнейший частный банк России',
            },
            {
                'name': 'ВТБ',
                'service_name': 'Услуги для самозанятых',
                'bank_type': 'state',
                'license_number': '1000', #
                'founded_year': 1990, #
                'years_existence': 36, #
                'branches_count': 38, #
                'atms_count': 144, #
                'financial_rating': 2, #
                'public_rating': 10, #
                'avg_customer_rating': 3.03, #
                'phone': '8-800-100-24-24', #
                'website': 'https://www.vtb.ru', #
                'support_online': True, #
                'description': 'Системообразующий банк с государственным участием',
            },
            {
                'name': 'Россельхозбанк',
                'service_name': 'Своё',
                'bank_type': 'state',
                'license_number': '3349', #
                'founded_year': 2000, #
                'years_existence': 26, #
                'branches_count': 7, #
                'atms_count': 11, #
                'financial_rating': 6, #
                'public_rating': 5, #
                'avg_customer_rating': 4.75, #
                'phone': '8-800-100-01-00', #
                'website': 'https://www.rshb.ru', #
                'support_online': True, #
                'description': 'Банк для агропромышленного комплекса',
            },
            {
                'name': 'МТС Банк',
                'service_name': 'МТС Деньги',
                'bank_type': 'private',
                'license_number': '2268', #
                'founded_year': 1993, #
                'years_existence': 33, #
                'branches_count': 2, #
                'atms_count': 5, #
                'financial_rating': 21, #
                'public_rating': 11, #
                'avg_customer_rating': 3.20, #
                'phone': '8-800-250-05-20', #
                'website': 'https://www.mtsbank.ru', #
                'support_online': True, #
                'description': 'Банк экосистемы МТС',
            },
            {
                'name': 'Райффайзен Банк',
                'service_name': 'Самозанятость',
                'bank_type': 'foreign',
                'license_number': '3292', #
                'founded_year': 1996, #
                'years_existence': 30, #
                'branches_count': 1, #
                'atms_count': 30, #
                'financial_rating': 11, #
                'public_rating': 43, #
                'avg_customer_rating': 3.07, #
                'phone': '8-800-700-17-17', #
                'website': 'https://www.raiffeisen.ru', #
                'support_online': True, #
                'description': 'Дочерний банк австрийской группы Raiffeisen',
            },
        ]

        created_banks = []
        for bank_data in banks_data:
            bank = Bank.objects.create(**bank_data)
            created_banks.append(bank)
            self.stdout.write(f'Создан банк: {bank.name}')

        # Данные сервисов
        services_data = [
            # Сбербанк
            {
                'bank': created_banks[0],
                'name': 'Своё дело', #
                'mobile_app': True, #
                'web_cabinet': True, #
                'onboarding_speed': 5, #
                'automatic_checks': True, #
                'cancel_checks': True, #
                'auto_tax_calculation': True, #
                'auto_tax_payment': True, #
                'income_statistics': True, #
                'limit_control': True, #
                'payment_by_phone': True, #
                'payment_by_qr': True, #
                'payment_by_details': True, #
                'sbp_integration': True, #
                'two_factor_auth': True, #
                'antifraud_automated': True, #
                'auto_logout': True, #
                'auto_logout_time': 5, #
                'support_online': True, #
                'monthly_fee_min': 0, #
                'monthly_fee_max': 0, #
                'internal_transfer_fee': 0, #
                'sbp_transfer_fee': 0.5, #
                'card_transfer_fee': 1, #
                'transfer_free_limit': 100000, #
                'cash_withdrawal_free_limit': 1000000, #
                'cash_withdrawal_fee': 2, #
                'deposit_free_limit': 'Безлимитно', #
                'deposit_fee': 0, #
                'international_transfers': True, #
                'international_countries': 'Абхазия, Азербайджан, Армения, Беларусь, Молдова, Таджикистан, Узбекистан, Филиппины, Индия, Танзания, Китай, Вьетнам', #
                'swift_available': False, #
            },
            # Т-Банк
            {
                'bank': created_banks[1],
                'name': 'Самозанятость', #
                'mobile_app': True, #
                'web_cabinet': True, #
                'onboarding_speed': 2, #
                'automatic_checks': False, #
                'cancel_checks': True, #
                'auto_tax_calculation': True, #
                'auto_tax_payment': True, #
                'income_statistics': False, #
                'limit_control': True, #
                'payment_by_phone': True, #
                'payment_by_qr': True, #
                'payment_by_details': True, #
                'sbp_integration': True, #
                'two_factor_auth': True, #
                'antifraud_automated': True, #
                'auto_logout': False, #
                'auto_logout_time': 0, #
                'support_online': True, #
                'monthly_fee_min': 0, #
                'monthly_fee_max': 0, #
                'internal_transfer_fee': 0, #
                'sbp_transfer_fee': 0.5, #
                'card_transfer_fee': 1.5, #
                'transfer_free_limit': 100000, #
                'cash_withdrawal_free_limit': 500000, #
                'cash_withdrawal_fee': 2, #
                'deposit_free_limit': 'Безлимитно', #
                'deposit_fee': 0, #
                'international_transfers': True, #
                'international_countries': 'Абхазия, Азербайджан, Армения, Беларусь, Казахстан, Кыргызстан, Приднестровье, Таджикистан, Тайланд, Узбекистан, Южная Осетия',
                'swift_available': False, #
            },
            # Альфа-Банк
            {
                'bank': created_banks[2],
                'name': 'Самозанятость', #
                'mobile_app': True, #
                'web_cabinet': True, #
                'onboarding_speed': 2, #
                'automatic_checks': True, #
                'cancel_checks': True, #
                'auto_tax_calculation': True, #
                'auto_tax_payment': True, #
                'income_statistics': True, #
                'limit_control': True, #
                'payment_by_phone': True, #
                'payment_by_qr': True, #
                'payment_by_details': True, #
                'sbp_integration': True,#
                'two_factor_auth': True, #
                'antifraud_automated': True,#
                'auto_logout': False, #
                'auto_logout_time': 0, #
                'support_online': True, #
                'monthly_fee_min': 0, #
                'monthly_fee_max': 0, #
                'internal_transfer_fee': 0, #
                'sbp_transfer_fee': 0.5, #
                'card_transfer_fee': 1.95, #
                'transfer_free_limit': 100000, #
                'cash_withdrawal_free_limit': 500000, #
                'cash_withdrawal_fee': 2,
                'deposit_free_limit': 'Безлимитно', #
                'deposit_fee': 0, #
                'international_transfers': True, #
                'international_countries': 'Беларусь, Таджикистан, Узбекистан, Казахстан, Вьетнам и др.',
                'swift_available': False, #
            },
            # ВТБ
            {
                'bank': created_banks[3],
                'name': 'Самозанятость', #
                'mobile_app': True, #
                'web_cabinet': True, #
                'onboarding_speed': 2, #
                'automatic_checks': True, #
                'cancel_checks': True, #
                'auto_tax_calculation': True, #
                'auto_tax_payment': True, #
                'income_statistics': True, #
                'limit_control': True, #
                'payment_by_phone': True, #
                'payment_by_qr': True, #
                'payment_by_details': True, #
                'sbp_integration': True, #
                'two_factor_auth': True, #
                'antifraud_automated': True, #
                'auto_logout': False, #
                'auto_logout_time': 0, #
                'support_online': True, #
                'monthly_fee_min': 0, #
                'monthly_fee_max': 0, #
                'internal_transfer_fee': 0, #
                'sbp_transfer_fee': 0.5, #
                'card_transfer_fee': 1.5, #
                'transfer_free_limit': 1000000, #
                'cash_withdrawal_free_limit': 2000000, #
                'cash_withdrawal_fee': 2,
                'deposit_free_limit': 'Безлимитно', #
                'deposit_fee': 0, #
                'international_transfers': True, #
                'international_countries': 'Казахстан, Узбекистан, Азербайджан, Кыргызстан, Китай, Германия',
                'swift_available': False, #
            },
            # Россельхозбанк
            {
                'bank': created_banks[4],
                'name': 'Всё для самозанятых', #
                'mobile_app': True, #
                'web_cabinet': True, #
                'onboarding_speed': 5, #
                'automatic_checks': True, #
                'cancel_checks': True, #
                'auto_tax_calculation': True, #
                'auto_tax_payment': True, #
                'income_statistics': True, #
                'limit_control': False, #
                'payment_by_phone': True, #
                'payment_by_qr': True, #
                'payment_by_details': True, #
                'sbp_integration': True, #
                'two_factor_auth': True, #
                'antifraud_automated': True, #
                'auto_logout': True, #
                'auto_logout_time': 15, #
                'support_online': True, #
                'monthly_fee_min': 0, #
                'monthly_fee_max': 0, #
                'internal_transfer_fee': 0, #
                'sbp_transfer_fee': 0.5, #
                'card_transfer_fee': 1.5, #
                'transfer_free_limit': 100000, #
                'cash_withdrawal_free_limit': 2000000, #
                'cash_withdrawal_fee': 1,
                'deposit_free_limit': 'Безлимитно', #
                'deposit_fee': 0, #
                'international_transfers': True, #
                'international_countries': 'Абхазия, Армения, Беларусь, Казахстан, Кыргызстан, Таджикистан, Узбекистан, Южная Осетия',
                'swift_available': False, #
            },
            # МТС Банк
            {
                'bank': created_banks[5],
                'name': 'Самозанятый', #
                'mobile_app': True, #
                'web_cabinet': True, #
                'onboarding_speed': 5, #
                'automatic_checks': True, #
                'cancel_checks': True, #
                'auto_tax_calculation': True, #
                'auto_tax_payment': True, #
                'income_statistics': True, #
                'limit_control': True, #
                'payment_by_phone': True, #
                'payment_by_qr': True, #
                'payment_by_details': True, #
                'sbp_integration': True, #
                'two_factor_auth': True, #
                'antifraud_automated': True, #
                'auto_logout': False, #
                'auto_logout_time': 0, #
                'support_online': True, #
                'monthly_fee_min': 0, #
                'monthly_fee_max': 0, #
                'internal_transfer_fee': 0, #
                'sbp_transfer_fee': 0.5, #
                'card_transfer_fee': 1.9, #
                'transfer_free_limit': 100000, #
                'cash_withdrawal_free_limit': 600000, #
                'cash_withdrawal_fee': 2,
                'deposit_free_limit': 'Безлимитно', #
                'deposit_fee': 0, #
                'international_transfers': True, #
                'international_countries': 'Азербайджан, Армения, Беларусь, Грузия, Казахстан, Китай, Кыргызстан, ОАЭ, Таджикистан, Таиланд, Турция, Узбекистан', #
                'swift_available': False, #
            },
            # Райффайзен Банк
            {
                'bank': created_banks[6],
                'name': 'Самозанятость', #
                'mobile_app': True, #
                'web_cabinet': True, #
                'onboarding_speed': 5, #
                'automatic_checks': False, #
                'cancel_checks': True, #
                'auto_tax_calculation': True, #
                'auto_tax_payment': False, #
                'income_statistics': True, #
                'limit_control': True, #
                'payment_by_phone': True, #
                'payment_by_qr': True, #
                'payment_by_details': True, #
                'sbp_integration': True, #
                'two_factor_auth': True, #
                'antifraud_automated': True, #
                'auto_logout': False, #
                'auto_logout_time': 0, #
                'support_online': True, #
                'monthly_fee_min': 0, #
                'monthly_fee_max': 0, #
                'internal_transfer_fee': 0, #
                'sbp_transfer_fee': 0.5, #
                'card_transfer_fee': 1.5, #
                'transfer_free_limit': 100000, #
                'cash_withdrawal_free_limit': 3000000, #
                'cash_withdrawal_fee': 1,
                'deposit_free_limit': 'Безлимитно', #
                'deposit_fee': 0, #
                'international_transfers': True, #
                'international_countries': 'СНГ (RUB, AMD, BYN)', #
                'swift_available': True, #
            },
        ]

        for service_data in services_data:
            service = DBOService.objects.create(**service_data)
            self.stdout.write(f'  Создан сервис: {service.name}')

        self.stdout.write(self.style.SUCCESS(f'Создано {len(created_banks)} банков, {len(services_data)} сервисов'))