"""
Пример использования Portal для работы с полями сущностей Bitrix24
"""
import asyncio
import os
import traceback
from fast_bitrix24 import Bitrix
from orm_bitrix24.entity import Portal
from pprint import pprint
from dotenv import load_dotenv
load_dotenv()

async def main():
    # Инициализация клиента Bitrix24
    webhook = os.getenv("WEBHOOK")
    if not webhook:
        print("Необходимо установить переменную окружения WEBHOOK")
        return
    
    bitrix = Bitrix(webhook)
    
    # Инициализация Portal
    portal = Portal(bitrix)
    
    # Получение всех полей сделки (включая пользовательские)
    # print("=== Получение всех полей сделки ===")
    # deal_fields = await portal.deal.fields.get_all()
    # print(f"Всего полей сделки: {len(deal_fields)}")
    
    # for field in deal_fields:  # Показываем первые 5 полей
    #     print(field.values)
    #     print(f"- {field.name}: {field.title} ({field.type})")
    #     if field.is_custom:
    #         # print(f'field: {field._data}')
    #         if field.type == 'enumeration':
    #             for value in field.values:
    #                 print(f'  {value.value} ({value.id})')
    #         print("  [Пользовательское поле]")
    # 1/0
    # Получение только пользовательских полей сделки
    # print("\n=== Пользовательские поля сделки ===")
    custom_fields = await portal.deal.fields.get_custom_fields()
    print(f"Пользовательских полей: {len(custom_fields)}")
    
    for field in custom_fields:
        print(f"- {field.name}: {field.title} ({field.type})")
        if field.type == 'enumeration':
            for value in field.values:
                print(f'  {value.value} ({value.id})')
    # 1/0
    # Создание нового пользовательского поля для сделки
    # print("\n=== Создание пользовательского поля ===")
    # try:
    #     new_field = await portal.deal.fields.create(
    #         field_name="TEST_FIELD",
    #         field_title="Тестовое поле",
    #         field_type="string",
    #         is_required=False
    #     )
    #     print(f"Создано поле: {new_field.name} - {new_field.title}")
    # except Exception as e:
    #     print(f"Ошибка при создании поля: {e}")
    
    # # Получение информации о конкретном поле
    # print("\n=== Получение информации о поле ===")
    # field_info = await portal.deal.fields.get_by_name("UF_CRM_TEST_FIELD")
    # if field_info:
    #     print(f"Поле UF_CRM_TEST_FIELD:")
    #     print(f"  Название: {field_info.title}")
    #     print(f"  Тип: {field_info.type}")
    #     print(f"  Обязательное: {field_info.is_required}")
    #     print(f"  Только чтение: {field_info.is_readonly}")
    # # 1/0
    # Работа с полями контактов
    print("\n=== Поля контактов ===")
    
    # Создание поля для контакта
    
    # contact_field = await portal.contact.fields.create(
    #     field_name="CONTACT_TEST",
    #     field_title="Тестовое поле контакта",
    #     field_type="string"
    # )
    # print(f"Создано поле контакта: {contact_field.name}")
    # # 1/0
    

    contact_fields = await portal.contact.fields.get_all()
    print(f"Всего полей контакта: {len(contact_fields)}")
    pprint(contact_fields)
    # # Получение полей всех сущностей одним запросом
    # print("\n=== Поля всех сущностей ===")
    # all_fields = await portal.get_all_entities_fields()
    # for entity_name, fields in all_fields.items():
    #     print(f"{entity_name.upper()}: {len(fields)} полей")
    # 1/0
    # Удаление созданных тестовых полей
    # print("\n=== Удаление тестовых полей ===")
    # try:
    #     deleted = await portal.deal.fields.delete("UF_CRM_TEST_FIELD")
    #     if deleted:
    #         print("Тестовое поле сделки удалено")
    #     else:
    #         print("Тестовое поле сделки не найдено или не удалено")
    # except Exception as e:
    #     print(f"Ошибка при удалении поля сделки: {e}")
    
    try:
        deleted = await portal.contact.fields.delete("UF_CRM_CONTACT_TEST")
        if deleted:
            print("Тестовое поле контакта удалено")
        else:
            print("Тестовое поле контакта не найдено или не удалено")
    except Exception as e:
        print(f"Ошибка при удалении поля контакта: {e}")


if __name__ == "__main__":
    asyncio.run(main()) 