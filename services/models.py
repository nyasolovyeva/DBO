from django.db import models
from .ahp import GLOBAL_WEIGHTS, calculate_saw_score

class Bank(models.Model):
    """Модель банка"""

    BANK_TYPES = [
        ('state', 'Государственный'),
        ('private', 'Частный'),
        ('foreign', 'Иностранный'),
    ]

    name = models.CharField('Название банка', max_length=200, unique=True)
    service_name = models.CharField('Название сервиса для самозанятых', max_length=200, blank=True)
    bank_type = models.CharField('Тип банка', max_length=20, choices=BANK_TYPES, default='private')

    # Лицензия и срок существования
    license_number = models.CharField('Номер лицензии ЦБ РФ', max_length=50, blank=True)
    founded_year = models.IntegerField('Год основания', null=True, blank=True)
    years_existence = models.IntegerField('Лет на рынке', null=True, blank=True)

    # Инфраструктура в Нижегородской области
    branches_count = models.IntegerField('Количество отделений в НО', default=0)
    atms_count = models.IntegerField('Количество банкоматов в НО', default=0)

    # Репутация и рейтинги
    financial_rating = models.IntegerField('Финансовый рейтинг (место)', null=True, blank=True)
    public_rating = models.IntegerField('Народный рейтинг (место)', null=True, blank=True)
    avg_customer_rating = models.FloatField('Средняя оценка клиентов', default=0)

    # Контакты
    phone = models.CharField('Телефон горячей линии', max_length=50, blank=True)
    website = models.URLField('Официальный сайт', blank=True)
    support_online = models.BooleanField('Круглосуточная онлайн-поддержка', default=True)

    description = models.TextField('Описание банка', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Банк'
        verbose_name_plural = 'Банки'
        ordering = ['name']
        db_table = 'services_bank'

    def __str__(self):
        return self.name

class DBOService(models.Model):
    """Модель сервиса ДБО для самозанятых"""

    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name='services', verbose_name='Банк')
    name = models.CharField('Название сервиса', max_length=200)

    # ==================== 1. МОБИЛЬНОЕ ПРИЛОЖЕНИЕ И ВЕБ-КАБИНЕТ ====================
    mobile_app = models.BooleanField('Мобильное приложение', default=False)
    web_cabinet = models.BooleanField('Веб-кабинет', default=False)

    # ==================== 2. СКОРОСТЬ ПОДКЛЮЧЕНИЯ ====================
    onboarding_speed = models.IntegerField('Скорость подключения (минут)', default=5)

    # ==================== 3. НАЛОГОВО-УЧЁТНАЯ ИНТЕГРАЦИЯ ====================
    automatic_checks = models.BooleanField('Автоматическое формирование чеков', default=False)
    cancel_checks = models.BooleanField('Отмена чеков', default=False)  # НОВЫЙ ФИЛЬТР
    auto_tax_calculation = models.BooleanField('Автоматический расчет налога', default=True)
    auto_tax_payment = models.BooleanField('Автоплатеж налога', default=False)

    # ==================== 4. ПЛАТЁЖНО-РАСЧЁТНЫЙ ФУНКЦИОНАЛ ====================
    payment_by_phone = models.BooleanField('Приём переводов по номеру телефона', default=True)
    payment_by_qr = models.BooleanField('Приём переводов по QR-коду', default=True)
    payment_by_details = models.BooleanField('Приём переводов по реквизитам', default=True)
    sbp_integration = models.BooleanField('Поддержка СБП', default=True)

    # ==================== 6. ДОПОЛНИТЕЛЬНЫЕ ЦИФРОВЫЕ СЕРВИСЫ ====================
    income_statistics = models.BooleanField('Наличие аналитики доходов', default=False)
    limit_control = models.BooleanField('Контроль лимита дохода', default=False)

    # ==================== 7. БЕЗОПАСНОСТЬ ====================
    two_factor_auth = models.BooleanField('Двухфакторная аутентификация', default=False)
    antifraud_automated = models.BooleanField('Антифрод-мониторинг', default=True)
    auto_logout = models.BooleanField('Автовыход при бездействии', default=True)
    auto_logout_time = models.IntegerField('Время автовыхода (мин)', default=5)

    # ==================== 8. ПОДДЕРЖКА ====================
    support_online = models.BooleanField('Круглосуточная поддержка 24/7', default=True)

    # ==================== 9. МЕЖДУНАРОДНЫЕ ПЕРЕВОДЫ ====================
    international_transfers = models.BooleanField('Доступны международные переводы', default=False)
    international_countries = models.TextField('Страны для переводов', blank=True)
    swift_available = models.BooleanField('SWIFT переводы', default=False)

    # ==================== 10. СТОИМОСТЬ ====================
    monthly_fee_min = models.DecimalField('Мин. плата (₽/мес)', max_digits=10, decimal_places=2, default=0)
    monthly_fee_max = models.DecimalField('Макс. плата (₽/мес)', max_digits=10, decimal_places=2, default=0)

    # ==================== 11. ПЕРЕВОДЫ ====================
    internal_transfer_fee = models.DecimalField('Внутрибанк комиссия (%)', max_digits=5, decimal_places=2, default=0)
    sbp_transfer_fee = models.DecimalField('СБП комиссия (%)', max_digits=5, decimal_places=2, default=0.5)
    card_transfer_fee = models.DecimalField('По карте комиссия (%)', max_digits=5, decimal_places=2, default=1.5)
    transfer_free_limit = models.IntegerField('Бесплатный лимит (₽/мес)', default=100000)

    # ==================== 12. СНЯТИЕ НАЛИЧНЫХ ====================
    cash_withdrawal_free_limit = models.IntegerField('Бесплатный лимит снятия (₽/мес)', default=100000)
    cash_withdrawal_fee = models.DecimalField('Комиссия за снятие сверх лимита (%)', max_digits=5, decimal_places=2,
                                              default=2)

    # ==================== 13. ВНЕСЕНИЕ НАЛИЧНЫХ ====================
    deposit_free_limit = models.CharField('Бесплатный лимит внесения (₽/мес)', max_length=200)
    deposit_fee = models.DecimalField('Комиссия за внесение сверх лимита (%)', max_digits=5, decimal_places=2,
                                      default=1)

    # AHP и SAW рейтинг
    ahp_rating = models.FloatField('AHP рейтинг', default=0)
    saw_rating = models.FloatField('SAW рейтинг', default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Сервис ДБО'
        verbose_name_plural = 'Сервисы ДБО'
        ordering = ['-ahp_rating', 'name']
        db_table = 'services_dboservice'

    def calculate_ahp_rating(self):
        score = 0.0

        score += self.get_monthly_fee_score() * GLOBAL_WEIGHTS["monthly_fee"]
        score += self.get_transfer_limit_score() * GLOBAL_WEIGHTS["transfer_limit"]

        score += int(self.auto_tax_calculation) * GLOBAL_WEIGHTS["auto_tax_calculation"]
        score += int(self.auto_tax_payment) * GLOBAL_WEIGHTS["auto_tax_payment"]
        score += int(self.automatic_checks) * GLOBAL_WEIGHTS["automatic_checks"]
        score += int(self.cancel_checks) * GLOBAL_WEIGHTS["cancel_checks"]

        score += int(self.payment_by_phone) * GLOBAL_WEIGHTS["payment_by_phone"]
        score += int(self.payment_by_qr) * GLOBAL_WEIGHTS["payment_by_qr"]
        score += int(self.payment_by_details) * GLOBAL_WEIGHTS["payment_by_details"]

        score += int(self.two_factor_auth) * GLOBAL_WEIGHTS["two_factor_auth"]
        score += int(self.antifraud_automated) * GLOBAL_WEIGHTS["antifraud_automated"]

        score += int(self.web_cabinet) * GLOBAL_WEIGHTS["web_cabinet"]
        score += int(self.mobile_app) * GLOBAL_WEIGHTS["mobile_app"]
        score += int(self.support_online) * GLOBAL_WEIGHTS["support_online"]

        score += int(self.income_statistics) * GLOBAL_WEIGHTS["income_statistics"]
        score += int(self.limit_control) * GLOBAL_WEIGHTS["limit_control"]

        return round(score, 6)

    def calculate_saw_rating(self):
        """
        Расчет рейтинга методом SAW с использованием весов из AHP
        """
        # Собираем оценки по всем критериям (0,1 или 0-1)
        scores = [
            self.get_monthly_fee_score(),
            self.get_transfer_limit_score(),
            int(self.auto_tax_calculation),
            int(self.auto_tax_payment),
            int(self.automatic_checks),
            int(self.cancel_checks),
            int(self.payment_by_phone),
            int(self.payment_by_qr),
            int(self.payment_by_details),
            int(self.two_factor_auth),
            int(self.antifraud_automated),
            int(self.web_cabinet),
            int(self.mobile_app),
            int(self.support_online),
            int(self.income_statistics),
            int(self.limit_control),
        ]

        # Веса из AHP в том же порядке
        weights = [
            GLOBAL_WEIGHTS["monthly_fee"],
            GLOBAL_WEIGHTS["transfer_limit"],
            GLOBAL_WEIGHTS["auto_tax_calculation"],
            GLOBAL_WEIGHTS["auto_tax_payment"],
            GLOBAL_WEIGHTS["automatic_checks"],
            GLOBAL_WEIGHTS["cancel_checks"],
            GLOBAL_WEIGHTS["payment_by_phone"],
            GLOBAL_WEIGHTS["payment_by_qr"],
            GLOBAL_WEIGHTS["payment_by_details"],
            GLOBAL_WEIGHTS["two_factor_auth"],
            GLOBAL_WEIGHTS["antifraud_automated"],
            GLOBAL_WEIGHTS["web_cabinet"],
            GLOBAL_WEIGHTS["mobile_app"],
            GLOBAL_WEIGHTS["support_online"],
            GLOBAL_WEIGHTS["income_statistics"],
            GLOBAL_WEIGHTS["limit_control"],
        ]

        return calculate_saw_score(scores, weights)

    def get_transfer_limit_score(self):
        """Возвращает вес лимита переводов для AHP"""
        if self.transfer_free_limit < 50000:
            return 0.0
        elif self.transfer_free_limit <= 100000:
            return 0.5
        else:
            return 1.0

    def get_monthly_fee_score(self):
        """Возвращает вес стоимости обслуживания для AHP"""
        if self.monthly_fee_min <= 99:
            return 1.0
        elif self.monthly_fee_min <= 149:
            return 0.5
        else:
            return 0.0

    def _get_onboarding_score(self):
        if self.onboarding_speed <= 2:
            return 5
        elif self.onboarding_speed <= 5:
            return 4
        elif self.onboarding_speed <= 10:
            return 3
        else:
            return 2

    def _get_fee_score(self):
        if self.monthly_fee_min == 0 and self.monthly_fee_max == 0:
            return 5
        elif self.monthly_fee_min <= 100:
            return 4
        elif self.monthly_fee_min <= 500:
            return 3
        elif self.monthly_fee_min <= 1000:
            return 2
        else:
            return 1

    def save(self, *args, **kwargs):
        self.ahp_rating = self.calculate_ahp_rating()
        self.saw_rating = self.calculate_saw_rating()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.bank.name} - {self.name}"