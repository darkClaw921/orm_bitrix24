"""
Тест для проверки получения пользовательских полей контактов
"""
import asyncio
import os
from fast_bitrix24 import Bitrix
from orm_bitrix24.entity import Portal
from dotenv import load_dotenv
load_dotenv()


async def test_contact_userfields():
    """Тест получения пользовательских полей контактов"""
    webhook = os.getenv("WEBHOOK")
    if not webhook:
        print("⚠️  Переменная WEBHOOK не установлена. Тест пропущен.")
        return
    
    try:
        # Инициализация
        bitrix = Bitrix(webhook)
        portal = Portal(bitrix)
        
        print("🔍 Получение полей контактов...")
        
        # Получаем все поля контакта (стандартные + пользовательские)
        contact_fields = await portal.contact.fields.get_all()
        
        print(f"✅ Получено {len(contact_fields)} полей контакта")
        
        # Разделяем на стандартные и пользовательские
        standard_fields = [field for field in contact_fields if not field.is_custom]
        custom_fields = [field for field in contact_fields if field.is_custom]
        
        print(f"\n📊 Статистика:")
        print(f"   Стандартных полей: {len(standard_fields)}")
        print(f"   Пользовательских полей: {len(custom_fields)}")
        
        # Показываем несколько стандартных полей
        print(f"\n📋 Стандартные поля (первые 5):")
        for field in standard_fields[:5]:
            print(f"   - {field.name}: {field.title} ({field.type})")
        
        # Показываем пользовательские поля
        if custom_fields:
            print(f"\n🔧 Пользовательские поля:")
            for field in custom_fields:
                print(f"   - {field.name}: {field.title} ({field.type})")
                
                # Если это enumeration поле, показываем значения
                if field.type == 'enumeration' and field.values:
                    print(f"     Значения ({len(field.values)}):")
                    for enum_value in field.values[:3]:  # Первые 3 значения
                        print(f"       • {enum_value.value} (ID: {enum_value.id})")
                    if len(field.values) > 3:
                        print(f"       ... и еще {len(field.values) - 3} значений")
        else:
            print(f"\n🔧 Пользовательские поля: отсутствуют")
        
        print(f"\n🎉 Тест завершен успешно!")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_contact_userfields()) 