"""
Пример работы с файловыми пользовательскими полями в ORM Bitrix24
"""

import asyncio
import os
from fast_bitrix24 import Bitrix
from orm_bitrix24.entity import _Deal, FileCustomField
from dotenv import load_dotenv
load_dotenv()

# Расширяем базовый класс Deal, добавляя файловые поля
class Deal(_Deal):
    documents = FileCustomField("UF_CRM_1749483343442", isMultiple=True)
    # contract = FileCustomField("UF_CRM_CONTRACT", isMultiple=False)


async def main():
    # Инициализация (замените на ваш webhook)
    webhook_url = os.getenv("WEBHOOK")
    if not webhook_url:
        print("Необходимо установить переменную окружения WEBHOOK")
        return
        
    bitrix = Bitrix(webhook_url)
    # Сохраняем webhook URL для доступа к файлам
    bitrix.webhook_url = webhook_url
    Deal.get_manager(bitrix)
    

    
    try:
        # Создаем новую сделку
        # deal: Deal = await Deal.objects.create(
        #     title="Тестовая сделка с файлами",
        #     opportunity=100000
        # )
        deal: Deal = await Deal.objects.get_by_id(221)
        print(f"Создана сделка ID: {deal.id}")
        
        # Создаем тестовые файлы для демонстрации
        test_files = []
        for i in range(2):
            filename = f"test_document_{i+1}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Это тестовый документ №{i+1} для сделки {deal.id}")
            test_files.append(filename)
        
        # Добавляем файлы в множественное поле
        print("\nДобавляем файлы в поле documents...")
        for file_path in test_files:
            deal.documents.append(file_path)
            print(f"Добавлен файл: {file_path}")
        
       
        
        # Сохраняем изменения
        await deal.save()
        print("\nФайлы успешно загружены в Bitrix24!")
        
        # Получаем информацию о загруженных файлах
        print("\nИнформация о файлах:")
        
        deal: Deal = await Deal.objects.get_by_id(deal.id)
        documents = deal.documents.get_all()
        print(f"Документы ({len(documents)} файлов):")
        for i, file in enumerate(documents, 1):
            print(f"  {i}. {file.name}")
            if file.download_url:
                print(f"     URL для скачивания: {file.download_url}")
        
        
        # Демонстрация скачивания файлов
        print("\nСкачивание файлов...")
        if documents:
            first_doc = documents[0]
            if first_doc.download_url:
                downloaded_path = await first_doc.download(f"downloaded_{first_doc.name}")
                if downloaded_path:
                    print(f"Файл скачан: {downloaded_path}")
        
        print(f"\nТестирование завершено. ID сделки: {deal.id}")
        
    except Exception as e:
        print(f"Ошибка: {e}")
    
    # finally:
    #     # Очищаем тестовые файлы
    #     cleanup_files = ["test_document_1.txt", "test_document_2.txt", "contract.txt"]
    #     for filename in cleanup_files:
    #         if os.path.exists(filename):
    #             os.remove(filename)
        
    #     # Очищаем скачанные файлы
    #     for filename in os.listdir("."):
    #         if filename.startswith("downloaded_"):
    #             os.remove(filename)


if __name__ == "__main__":
    asyncio.run(main()) 