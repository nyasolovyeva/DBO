import numpy as np

def add_normalized_weights(crit):
    weights = np.prod(crit, axis=1) ** (1 / len(crit))
    normalized_weights = weights / np.sum(weights)
    return np.column_stack([crit, normalized_weights])

def add_global_weights(crit, lok_weight_krit):
    glob_weight = crit[:, -1] * lok_weight_krit
    return np.column_stack([crit, glob_weight])

def build_ahp_matrices():
    #Матрица критериев
    criterii = np.array([
        [1,3,5,3,3,5],          #Налогово-учётная интеграция
        [1/3,1,3,3,3,5],        #Платёжно-расчётный функционал
        [1/5,1/3,1,1/5,1/3,3],  #Стоимость банковского обслуживания
        [1/3,1/3,5,1,3,5],      #Безопасность дистанционного обслуживания
        [1/3,1/3,3,1/3,1,3],    #Удобство использования сервиса
        [1/5,1/5,1/3,1/5,1/3,1] #Дополнительные цифровые сервисы
    ])
    criterii = add_normalized_weights(criterii)

    #Подкритерии

    #Налогово-учётная интеграция
    NYI = np.array([
        [1,3,1/3,5],    #Автоматический расчёт налога
        [1/3,1,1/5,3],  #Автоматическая оплата налога
        [3,5,1,5],      #Автоматическое формирование чеков
        [1/5,1/3,1/5,1] #Отмена чеков
    ])
    NYI = add_normalized_weights(NYI)
    NYI = add_global_weights(NYI, criterii[0][-1])

    #Платёжно-расчётный функционал
    PRF = np.array([
        [1,1,3],    #Приём переводов по номеру телефона
        [1,1,3],    #Приём переводов по QR-коду
        [1/3,1/3,1] #Приём переводов по реквизитам
    ])
    PRF = add_normalized_weights(PRF)
    PRF = add_global_weights(PRF, criterii[1][-1])

    #Стоимость банковского обслуживания
    SBO = np.array([
        [1,3],  #Стоимость обслуживания сервиса
        [1/3,1] #Лимиты на переводы
    ])
    SBO = add_normalized_weights(SBO)
    SBO = add_global_weights(SBO, criterii[2][-1])

    #Безопасность дистанционного обслуживания
    BDO = np.array([
        [1,1],  #Двухфакторная аутентификация
        [1,1]   #Антифрод-мониторинг
    ])
    BDO = add_normalized_weights(BDO)
    BDO = add_global_weights(BDO, criterii[3][-1])

    #Удобство использования сервиса
    YIS = np.array([
        [1,1/3,3],  #Веб-кабинет
        [3,1,5],    #Мобильное приложение
        [1/3,1/5,1] #Поддержка 24/7
    ])
    YIS = add_normalized_weights(YIS)
    YIS = add_global_weights(YIS, criterii[4][-1])

    #Дополнительные цифровые сервисы
    DCS = np.array([
        [1,1/3],    #Наличие аналитики доходов
        [3,1]       #Контроль лимита дохода
    ])
    DCS = add_normalized_weights(DCS)
    DCS = add_global_weights(DCS, criterii[5][-1])

    return {
        "criterii": criterii,
        "NYI": NYI,
        "PRF": PRF,
        "SBO": SBO,
        "BDO": BDO,
        "YIS": YIS,
        "DCS": DCS,
    }

AHP_DATA = build_ahp_matrices()

def get_global_weights():
    data = build_ahp_matrices()

    return {
        "auto_tax_calculation": data["NYI"][0, -1],
        "auto_tax_payment": data["NYI"][1, -1],
        "automatic_checks": data["NYI"][2, -1],
        "cancel_checks": data["NYI"][3, -1],

        "payment_by_phone": data["PRF"][0, -1],
        "payment_by_qr": data["PRF"][1, -1],
        "payment_by_details": data["PRF"][2, -1],

        "monthly_fee": data["SBO"][0, -1],
        "transfer_limit": data["SBO"][1, -1],

        "two_factor_auth": data["BDO"][0, -1],
        "antifraud_automated": data["BDO"][1, -1],

        "web_cabinet": data["YIS"][0, -1],
        "mobile_app": data["YIS"][1, -1],
        "support_online": data["YIS"][2, -1],

        "income_statistics": data["DCS"][0, -1],
        "limit_control": data["DCS"][1, -1],
    }

GLOBAL_WEIGHTS = get_global_weights()


def calculate_saw_score(scores, weights):
    """
    Расчет итоговой оценки методом SAW

    Args:
        scores: список оценок альтернативы по критериям
        weights: список весов критериев (сумма = 1)

    Returns:
        Итоговая оценка (0-1)
    """
    # Максимальная нормализация (деление на максимальное значение по критерию)
    max_score = max(scores) if scores else 1
    normalized = [s / max_score for s in scores]

    # Взвешенная сумма
    return sum(n * w for n, w in zip(normalized, weights))