"""
Пример использования сущности Activity для работы с делами CRM в Bitrix24

Этот файл демонстрирует использование новой функциональности
для создания и управления активностями (звонки, встречи, email).
"""

import asyncio
import os
from loguru import logger
from fast_bitrix24 import Bitrix
# Импортируем необходимые классы
from orm_bitrix24.entity import _Deal, Activity, EmailActivity
from dotenv import load_dotenv

load_dotenv()


class Deal(_Deal):
    """Расширенный класс Deal с поддержкой активностей"""
    pass


async def activity_example():
    """Пример работы с активностями"""
    from pprint import pprint
    # Инициализация
    webhook_url = os.getenv('WEBHOOK')
    if not webhook_url:
        logger.error("Не установлена переменная окружения WEBHOOK")
        return
    
    bitrix = Bitrix(webhook_url)
    
    # Инициализация менеджера сделок
    Deal.get_manager(bitrix)
    # ActivityManager создается автоматически при создании объекта Deal
    
    try:
        # Получаем первую сделку для демонстрации
        deals = await Deal.objects.get_all()
        if not deals:
            logger.warning("Нет доступных сделок для тестирования")
            return
        
        deal = deals[0]
        logger.info(f"Работаем со сделкой: {deal.title} (ID: {deal.id})")

        # Получение всех активностей сделки
        logger.info("=== Получение всех активностей сделки ===")
        all_activities = await deal.activity.get_all()
        logger.info(f"Найдено {len(all_activities)} активностей для сделки")
        
        for activity in all_activities[-3:]:  # Показываем последние 3
            logger.info(f"- {activity.subject} (Тип: {activity.type_id}, ID: {activity.id})")
        
        # if all_activities:
            # pprint(all_activities[0]._data)
        
        # Демонстрация создания email-активности для контакта сделки
        logger.info("=== Создание email-активности для контакта сделки ===")
        
        # Сначала получаем контакт из сделки
        if deal.contact_id:
            logger.info(f"Отправляем письмо контакту из сделки (ID: {deal.contact_id})")
            email_activity = await deal.activity.mail(
                subject="Коммерческое предложение из ORM просто ответьте",
                message="Добрый день! Высылаем коммерческое предложение через новую ORM-систему.",
                contact_id=deal.contact_id,
                from_email="darkclaw921@yandex.ru"
                
             
            )
        else:
            pass
        
        
        logger.success(f"Email-активность создана: {email_activity}")
        logger.info(f"Получатель: {email_activity.to_email}")
        1/0
        # Демонстрация создания письма на произвольный email
        logger.info("=== Создание письма на произвольный email ===")
        custom_email_activity = await deal.activity.mail(
            subject="Письмо на внешний email",
            message="Это письмо отправляется на внешний email адрес",
            to_email="external@client.com"
        )
        logger.success(f"Письмо на внешний email создано: {custom_email_activity}")
        
        # Демонстрация создания звонка
        logger.info("=== Создание активности-звонка ===")
        call_activity = await deal.activity.create_call(
            subject="Тестовый звонок",
            phone="+7999123456",
            description="Звонок создан через ORM систему",
            direction=2,  # Исходящий
            completed=False
        )
        logger.success(f"Звонок создан: {call_activity}")
        
        # Демонстрация создания встречи
        logger.info("=== Создание активности-встречи ===")
        meeting_activity = await deal.activity.create_meeting(
            subject="Тестовая встреча",
            location="Офис тестирования",
            description="Встреча для демонстрации ORM функциональности"
        )
        logger.success(f"Встреча создана: {meeting_activity}")
        
        # Получение всех активностей сделки
        logger.info("=== Получение всех активностей сделки ===")
        all_activities = await deal.activity.get_all()
        logger.info(f"Найдено {len(all_activities)} активностей для сделки")
        
        for activity in all_activities[-3:]:  # Показываем последние 3
            logger.info(f"- {activity.subject} (Тип: {activity.type_id}, ID: {activity.id})")
        
        # Отметить звонок как выполненный
        logger.info("=== Завершение звонка ===")
        await call_activity.complete()
        logger.success("Звонок отмечен как выполненный")
        
        # Фильтрация активностей (требует инициализации Activity.objects)
        logger.info("=== Фильтрация активностей ===")
        Activity.get_manager(bitrix)  # Инициализируем менеджер для фильтрации
        email_activities = await Activity.objects.filter(
            entity_type='DEAL',
            entity_id=deal.id,
            type_id=4  # Email активности
        )
        logger.info(f"Найдено {len(email_activities)} email-активностей")
        
        # Демонстрация доступа к email данным
        if email_activities:
            for email_act in email_activities:
                if isinstance(email_act, EmailActivity):
                    logger.info(f"Email активность: {email_act.subject} -> {email_act.to_email}")
                else:
                    logger.info(f"Активность: {email_act.subject} (тип {email_act.type_id})")
        
    except Exception as e:
        logger.error(f"Ошибка при работе с активностями: {e}")
        raise


if __name__ == "__main__":
    logger.info("Запуск примера работы с активностями")
    asyncio.run(activity_example()) 