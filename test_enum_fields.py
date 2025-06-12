"""
Тест для проверки работы с полями enumeration
"""
import asyncio
import os
from fast_bitrix24 import Bitrix
from orm_bitrix24.entity import Portal
from dotenv import load_dotenv
load_dotenv()


async def test_enum_fields():
    """Тест работы с полями enumeration"""
    webhook = os.getenv("WEBHOOK")
    if not webhook:
        print("⚠️  Переменная WEBHOOK не установлена. Тест пропущен.")
        return
    
    try:
        # Инициализация
        bitrix = Bitrix(webhook)
        portal = Portal(bitrix)
        
        print("🔍 Поиск полей типа enumeration...")
        
        # Получаем все поля сделки
        deal_fields = await portal.deal.fields.get_all()
        
        # Ищем поля типа enumeration
        enum_fields = [field for field in deal_fields if field.type == 'enumeration']
        
        print(f"✅ Найдено {len(enum_fields)} полей типа enumeration")
        
        for field in enum_fields:
            print(f"\n📋 Поле: {field.name}")
            print(f"   Название: {field.title}")
            print(f"   Тип: {field.type}")
            print(f"   Пользовательское: {field.is_custom}")
            
            if field.values:
                print(f"   Значения ({len(field.values)}):")
                for enum_value in field.values:
                    print(f"     - {enum_value.value} (ID: {enum_value.id})")
            else:
                print("   Значения: отсутствуют")
        
        # Проверим также другие сущности
        print(f"\n🔍 Проверка полей contact...")
        contact_fields = await portal.contact.fields.get_all()
        contact_enum_fields = [field for field in contact_fields if field.type == 'enumeration']
        print(f"✅ В контактах найдено {len(contact_enum_fields)} enumeration полей")
        
        for field in contact_enum_fields[:2]:  # Показываем первые 2
            print(f"   📋 {field.name}: {field.title} ({len(field.values)} значений)")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(test_enum_fields()) 