from django import forms


class BankFilterForm(forms.Form):
    """Форма для фильтрации банков и сервисов"""

    SORT_CHOICES = [
        ('ahp_desc', 'По оценке (высокая → низкая)'),
        ('ahp_asc', 'По оценке (низкая → высокая)'),
        ('price_asc', 'По стоимости (дешевле → дороже)'),
        ('price_desc', 'По стоимости (дороже → дешевле)'),
        ('name_asc', 'По названию (А-Я)'),
        ('name_desc', 'По названию (Я-А)'),
    ]

    BANK_TYPES = [
        ('', 'Все банки'),
        ('state', 'Государственные'),
        ('private', 'Частные'),
        ('foreign', 'Иностранные'),
    ]

    query = forms.CharField(
        label='Поиск',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Название банка или сервиса...'
        })
    )

    sort_by = forms.ChoiceField(
        label='Сортировать',
        choices=SORT_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    bank_type = forms.ChoiceField(
        label='Тип банка',
        choices=BANK_TYPES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    min_ahp_rating = forms.FloatField(
        label='Мин. оценка сервиса',
        required=False,
        min_value=0,
        max_value=10,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'от 0 до 10'
        })
    )

    max_monthly_fee = forms.DecimalField(
        label='Макс. стоимость',
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '₽/мес'
        })
    )

    min_transfer_limit = forms.IntegerField(
        label='Мин. лимит переводов (₽/мес)',
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'от 0 ₽'
        })
    )

    # ==================== НАЛОГОВО-УЧЁТНАЯ ИНТЕГРАЦИЯ ====================
    auto_tax_calculation = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    auto_tax_payment = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    automatic_checks = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    cancel_checks = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    # ==================== ПЛАТЁЖНО-РАСЧЁТНЫЙ ФУНКЦИОНАЛ ====================
    payment_by_phone = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    payment_by_qr = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    payment_by_details = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    # ==================== БЕЗОПАСНОСТЬ ====================
    two_factor_auth = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    antifraud_automated = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    # ==================== ДОПОЛНИТЕЛЬНЫЕ ЦИФРОВЫЕ СЕРВИСЫ ====================
    income_statistics = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    limit_control = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    # ==================== УДОБСТВО ИСПОЛЬЗОВАНИЯ ====================
    mobile_app = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    web_cabinet = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    support_online = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )