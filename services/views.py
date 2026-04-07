from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count, Prefetch
from .models import Bank, DBOService
from .forms import BankFilterForm


def get_selected_filters(form):
    """Собирает выбранные пользователем фильтры"""
    selected = []

    if form.is_valid():
        # Налогово-учётная интеграция
        if form.cleaned_data.get('auto_tax_calculation'):
            selected.append('auto_tax_calculation')
        if form.cleaned_data.get('auto_tax_payment'):
            selected.append('auto_tax_payment')
        if form.cleaned_data.get('automatic_checks'):
            selected.append('automatic_checks')
        if form.cleaned_data.get('cancel_checks'):
            selected.append('cancel_checks')

        # Платёжно-расчётный функционал
        if form.cleaned_data.get('payment_by_phone'):
            selected.append('payment_by_phone')
        if form.cleaned_data.get('payment_by_qr'):
            selected.append('payment_by_qr')
        if form.cleaned_data.get('payment_by_details'):
            selected.append('payment_by_details')

        # Безопасность
        if form.cleaned_data.get('two_factor_auth'):
            selected.append('two_factor_auth')
        if form.cleaned_data.get('antifraud_automated'):
            selected.append('antifraud_automated')

        # Дополнительные цифровые сервисы
        if form.cleaned_data.get('income_statistics'):
            selected.append('income_statistics')
        if form.cleaned_data.get('limit_control'):
            selected.append('limit_control')

        # Удобство использования
        if form.cleaned_data.get('mobile_app'):
            selected.append('mobile_app')
        if form.cleaned_data.get('web_cabinet'):
            selected.append('web_cabinet')
        if form.cleaned_data.get('support_online'):
            selected.append('support_online')

        min_transfer_limit = form.cleaned_data.get('min_transfer_limit')
        if min_transfer_limit is not None and min_transfer_limit > 0:
            selected.append('transfer_limit')

        max_monthly_fee = form.cleaned_data.get('max_monthly_fee')
        if max_monthly_fee is not None and max_monthly_fee > 0:
            selected.append('monthly_fee')

    return selected


def calculate_dynamic_ahp_rating(service, selected_filters):
    """
    Динамический AHP рейтинг (только по выбранным фильтрам)
    """
    if not selected_filters:
        return service.ahp_rating

    from .ahp import GLOBAL_WEIGHTS

    score = 0.0
    total_weight = 0.0

    for criterion in selected_filters:
        weight = GLOBAL_WEIGHTS.get(criterion, 0)

        # Для разных критериев берем разные значения
        if criterion == 'monthly_fee':
            value = service.get_monthly_fee_score()
        elif criterion == 'transfer_limit':
            value = service.get_transfer_limit_score()
        else:
            value = int(getattr(service, criterion, False))

        score += value * weight
        total_weight += weight

    if total_weight > 0:
        return score / total_weight
    return 0.0


def calculate_dynamic_saw_rating(service, selected_filters):
    """
    Динамический SAW рейтинг (только по выбранным фильтрам)
    """
    if not selected_filters:
        return service.saw_rating

    from .ahp import GLOBAL_WEIGHTS

    score = 0.0
    total_weight = 0.0

    for criterion in selected_filters:
        weight = GLOBAL_WEIGHTS.get(criterion, 0)

        if criterion == 'monthly_fee':
            value = service.get_monthly_fee_score()
        elif criterion == 'transfer_limit':
            value = service.get_transfer_limit_score()
        else:
            value = int(getattr(service, criterion, False))

        score += value * weight
        total_weight += weight

    if total_weight > 0:
        return score / total_weight
    return 0.0


def bank_list(request):
    """Список банков с таблицей сервисов и динамическим рейтингом"""

    services = DBOService.objects.select_related('bank').all()
    form = BankFilterForm(request.GET or None)

    # Фильтрация
    if form.is_valid():
        query = form.cleaned_data.get('query')
        if query:
            services = services.filter(
                Q(name__icontains=query) | Q(bank__name__icontains=query)
            )

        bank_type = form.cleaned_data.get('bank_type')
        if bank_type:
            services = services.filter(bank__bank_type=bank_type)

        min_ahp_rating = form.cleaned_data.get('min_ahp_rating')
        if min_ahp_rating:
            services = services.filter(ahp_rating__gte=min_ahp_rating / 10)

        max_monthly_fee = form.cleaned_data.get('max_monthly_fee')
        if max_monthly_fee:
            services = services.filter(monthly_fee_max__lte=max_monthly_fee)

        # Фильтрация по чекбоксам (оставляем только сервисы с выбранными функциями)
        if form.cleaned_data.get('auto_tax_calculation'):
            services = services.filter(auto_tax_calculation=True)
        if form.cleaned_data.get('auto_tax_payment'):
            services = services.filter(auto_tax_payment=True)
        if form.cleaned_data.get('automatic_checks'):
            services = services.filter(automatic_checks=True)
        if form.cleaned_data.get('cancel_checks'):
            services = services.filter(cancel_checks=True)

        if form.cleaned_data.get('payment_by_phone'):
            services = services.filter(payment_by_phone=True)
        if form.cleaned_data.get('payment_by_qr'):
            services = services.filter(payment_by_qr=True)
        if form.cleaned_data.get('payment_by_details'):
            services = services.filter(payment_by_details=True)

        if form.cleaned_data.get('two_factor_auth'):
            services = services.filter(two_factor_auth=True)
        if form.cleaned_data.get('antifraud_automated'):
            services = services.filter(antifraud_automated=True)

        if form.cleaned_data.get('income_statistics'):
            services = services.filter(income_statistics=True)
        if form.cleaned_data.get('limit_control'):
            services = services.filter(limit_control=True)

        if form.cleaned_data.get('mobile_app'):
            services = services.filter(mobile_app=True)
        if form.cleaned_data.get('web_cabinet'):
            services = services.filter(web_cabinet=True)
        if form.cleaned_data.get('support_online'):
            services = services.filter(support_online=True)

    # Получаем выбранные фильтры для динамического расчета
    selected_filters = get_selected_filters(form)

    # Получаем банки с сервисами
    banks = Bank.objects.prefetch_related(
        Prefetch('services', queryset=services)
    ).annotate(
        services_count=Count('services')
    ).filter(services_count__gt=0)

    banks_list = list(banks)

    # Добавляем динамические рейтинги каждому сервису
    for bank in banks_list:
        for service in bank.services.all():
            # Динамический AHP рейтинг
            service.dynamic_ahp = calculate_dynamic_ahp_rating(service, selected_filters)
            # Динамический SAW рейтинг
            service.dynamic_saw = calculate_dynamic_saw_rating(service, selected_filters)
            # Для отображения в 10-балльной шкале
            service.dynamic_ahp_10 = service.dynamic_ahp * 10
            service.dynamic_saw_10 = service.dynamic_saw * 10

            # Статический рейтинг (для информации)
            service.rating_10 = service.ahp_rating * 10

    # СОРТИРОВКА по динамическому рейтингу
    sort_by = form.cleaned_data.get('sort_by') if form.is_valid() else None

    if sort_by == 'ahp_desc':
        for bank in banks_list:
            bank.max_rating = max([s.dynamic_ahp for s in bank.services.all()], default=0)
        banks_list.sort(key=lambda b: b.max_rating, reverse=True)
    elif sort_by == 'ahp_asc':
        for bank in banks_list:
            bank.max_rating = max([s.dynamic_ahp for s in bank.services.all()], default=0)
        banks_list.sort(key=lambda b: b.max_rating)
    elif sort_by == 'saw_desc':
        for bank in banks_list:
            bank.max_rating = max([s.dynamic_saw for s in bank.services.all()], default=0)
        banks_list.sort(key=lambda b: b.max_rating, reverse=True)
    elif sort_by == 'saw_asc':
        for bank in banks_list:
            bank.max_rating = max([s.dynamic_saw for s in bank.services.all()], default=0)
        banks_list.sort(key=lambda b: b.max_rating)
    elif sort_by == 'price_asc':
        banks_list.sort(key=lambda b: min([s.monthly_fee_min for s in b.services.all()], default=0))
    elif sort_by == 'price_desc':
        banks_list.sort(key=lambda b: max([s.monthly_fee_max for s in b.services.all()], default=0), reverse=True)
    elif sort_by == 'name_asc':
        banks_list.sort(key=lambda b: b.name)
    elif sort_by == 'name_desc':
        banks_list.sort(key=lambda b: b.name, reverse=True)

    context = {
        'form': form,
        'banks': banks_list,
        'banks_count': len(banks_list),
        'total_services': services.count(),
        'selected_filters': selected_filters,
    }

    return render(request, 'services/bank_list.html', context)


def service_detail(request, pk):
    """Детальная страница сервиса"""

    service = get_object_or_404(
        DBOService.objects.select_related('bank'),
        pk=pk
    )

    service.rating_10 = service.ahp_rating * 10

    context = {
        'service': service,
    }

    return render(request, 'services/service_detail.html', context)


def compare_services(request):
    """Сравнение нескольких сервисов"""

    service_ids = request.GET.getlist('ids')

    # Получаем выбранные сервисы из базы данных
    services = DBOService.objects.filter(id__in=service_ids).select_related('bank') if service_ids else []

    # Для каждого сервиса рассчитываем динамический SAW рейтинг
    for service in services:
        # Вызываем готовую функцию calculate_dynamic_saw_rating
        # Передаем пустой список [] - значит считаем по ВСЕМ критериям
        service.dynamic_saw = calculate_dynamic_saw_rating(service, [])
        # Переводим в 10-балльную шкалу
        service.dynamic_saw_10 = service.dynamic_saw * 10

        # Для информации оставляем статический AHP рейтинг
        service.rating_10 = service.ahp_rating * 10

    context = {
        'services': services,
    }

    return render(request, 'services/compare.html', context)