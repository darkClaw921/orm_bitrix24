#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import os
from fast_bitrix24 import Bitrix
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

# Настраиваем логирование
logger.add("timeline_example.log", rotation="10 MB", level="DEBUG")

# Импортируем классы из ORM
from orm_bitrix24.entity import _Deal as Deal, _Lead as Lead, TimelineComment

async def main():
    # Получаем вебхук из переменной окружения
    webhook = os.environ.get("WEBHOOK")
    if not webhook:
        logger.error("Необходимо установить переменную окружения WEBHOOK")
        return
    
    # Инициализируем клиент Bitrix24
    bitrix = Bitrix(webhook)
    
    # Инициализируем менеджеры
    Deal.get_manager(bitrix)
    Lead.get_manager(bitrix)
    TimelineComment.get_manager(bitrix)
    
    # Получаем сделку по ID
    deal_id = 239  # замените на реальный ID сделки
    deal = await Deal.objects.get_by_id(deal_id)
    if not deal:
        logger.error(f"Сделка с ID {deal_id} не найдена")
        return
    
    # Выводим информацию о сделке
    logger.info(f"Сделка: {deal.title} (ID: {deal.id})")
    
    # Работа с таймлайном сделки
    
    # 1. Получение всех комментариев
    logger.info("Получение комментариев из таймлайна...")
    comments = await deal.timeline.comments.get_all()
    logger.info(f"Найдено {len(comments)} комментариев")
    
    # Вывод информации о каждом комментарии
    for i, comment in enumerate(comments, 1):
        logger.info(f"Комментарий {i}: {comment.comment} (Автор: {comment.author_id}, Дата: {comment.created})")
    
    # 2. Добавление нового комментария
    logger.info("Добавление комментария в таймлайн...")
    new_comment = await deal.timeline.comments.create(
        comment="Тестовый комментарий из ORM-системы"
    )
    logger.success(f"Добавлен комментарий с ID: {new_comment.id}")
    
    # 3. Добавление лог-записи в таймлайн
    logger.info("Добавление лог-записи в таймлайн...")
    log_entry = await deal.timeline.add_log_message(
        title="Тестовая запись",
        text="Это тестовая запись в таймлайне сделки",
        icon_code="info" # Опциональный код иконки
    )
    logger.success(f"Добавлена лог-запись с ID: {log_entry['id']}")
    
    # Получаем лид по ID
    lead_id = 456  # замените на реальный ID лида
    lead = await Lead.objects.get_by_id(lead_id)
    if not lead:
        logger.error(f"Лид с ID {lead_id} не найден")
        return
    
    # Работа с таймлайном лида
    logger.info(f"Лид: {lead.title} (ID: {lead.id})")
    
    # Добавление комментария в таймлайн лида
    logger.info("Добавление комментария в таймлайн лида...")
    lead_comment = await lead.timeline.comments.create(
        comment="Тестовый комментарий к лиду из ORM-системы"
    )
    logger.success(f"Добавлен комментарий к лиду с ID: {lead_comment.id}")
    
    # Получение комментариев из таймлайна лида
    lead_comments = await lead.timeline.comments.get_all()
    logger.info(f"Найдено {len(lead_comments)} комментариев в таймлайне лида")

if __name__ == "__main__":
    asyncio.run(main()) 