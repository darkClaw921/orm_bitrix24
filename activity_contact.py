
import asyncio
import os
from loguru import logger
from fast_bitrix24 import Bitrix
# Импортируем необходимые классы
from orm_bitrix24.entity import _Deal, Activity, EmailActivity, TextCustomField
from dotenv import load_dotenv

load_dotenv()


class Deal(_Deal):
    """Расширенный класс Deal с поддержкой активностей"""
    test_field = TextCustomField("UF_CRM_1748463696180")
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
    

    # Получаем первый контакт для демонстрации
    deal :Deal = await Deal.objects.get_by_id(239)
    # deal=await Deal.objects.get_by_id(239)
    
  
    
    logger.info(f"Работаем со сделкой: {deal.title} (ID: {deal.id})")

    # Получение всех активностей сделки
    # logger.info("=== Получение всех активностей сделки ===")
    # all_activities = await deal.activity.get_all()
    # logger.info(f"Найдено {len(all_activities)} активностей для сделки")
    
    # for activity in all_activities[-3:]:  # Показываем последние 3
    #     logger.info(f"- {activity.subject} (Тип: {activity.type_id}, ID: {activity.id})")
    
    
    # comments = await deal.timeline.comments.get_all()
    # logger.info(f"Найдено {len(comments)} комментариев таймлайна")
    # for comment in comments:
    #     logger.info(f"Комментарий ID {comment.id}: {comment.comment} от {comment.author_id}")
    
    # new_comment = await deal.timeline.comments.create("Тестовый комментарий через ORM2")
    # logger.success(f"Создан новый комментарий с ID: {new_comment.id}")

    await deal.contact
    
    # await deal.contact.timeline.comments.create("Тестовый комментарий через ORM3")
    comments = await deal.contact.timeline.comments.get_all()
    logger.info(f"Найдено {len(comments)} комментариев таймлайна")
    for comment in comments:
        logger.info(f"Комментарий ID {comment.id}: {comment.comment} от {comment.author_id}")
    
    
if __name__ == "__main__":
    asyncio.run(activity_example())