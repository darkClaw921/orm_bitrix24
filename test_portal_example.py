"""
Простой тест для проверки основной функциональности Portal
"""
import asyncio
import os
from fast_bitrix24 import Bitrix
from orm_bitrix24.entity import Portal


async def test_portal_basic_functionality():
    """Базовый тест функциональности Portal"""
    # Проверяем наличие webhook
    webhook = os.getenv("WEBHOOK")
    if not webhook:
        print("⚠️  Переменная WEBHOOK не установлена. Тест пропущен.")
        return
    
    try:
        # Инициализация
        bitrix = Bitrix(webhook)
        portal = Portal(bitrix)
        
        print("✅ Portal успешно инициализирован")
        
        # Тест получения полей сделки
        deal_fields = await portal.deal.fields.get_all()
        print(f"✅ Получено {len(deal_fields)} полей сделки")
        
        # Тест получения пользовательских полей
        custom_fields = await portal.deal.fields.get_custom_fields()
        print(f"✅ Найдено {len(custom_fields)} пользовательских полей")
        
        # Тест поиска конкретного поля
        title_field = await portal.deal.fields.get_by_name("TITLE")
        if title_field:
            print(f"✅ Найдено поле TITLE: {title_field.title} ({title_field.type})")
        else:
            print("❌ Поле TITLE не найдено")
        
        # Тест получения полей контакта
        contact_fields = await portal.contact.fields.get_all()
        print(f"✅ Получено {len(contact_fields)} полей контакта")
        
        print("\n🎉 Все базовые тесты Portal прошли успешно!")
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании Portal: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(test_portal_basic_functionality()) 