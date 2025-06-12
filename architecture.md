# Архитектура ORM для Bitrix24

## Описание

ORM-система для работы с сущностями Bitrix24 через API. Обеспечивает удобный объектно-ориентированный интерфейс для работы с сущностями CRM.

## Структура проекта

### Структура директорий и файлов

```
orm_bitrix24/
  ├── entity/                  # Модуль с ORM-классами
  │   ├── __init__.py          # Инициализация модуля
  │   ├── base.py              # Базовые классы для ORM
  │   ├── company.py           # Класс для работы с компаниями
  │   ├── contact.py           # Класс для работы с контактами 
  │   ├── deal.py              # Базовый класс для работы со сделками
  │   ├── deal.pyi             # Stub-файл для автодополнения в IDE
  │   ├── lead.py              # Класс для работы с лидами
  │   ├── note.py              # Класс для работы с примечаниями
  │   ├── activity.py          # Классы для работы с делами CRM
  │   ├── timeline.py          # Классы для работы с таймлайном
  │   └── portal.py            # Классы для работы с порталом и полями сущностей
  ├── tests/                   # Модуль с тестами
  │   ├── conftest.py          # Конфигурация pytest
  │   └── test_deal.py         # Тесты для сделок
  ├── main.py                  # Пример использования ORM
  ├── portal_example.py        # Пример использования Portal для работы с полями
  └── pyproject.toml           # Конфигурация проекта
```

## Описание модулей

### entity/base.py
Базовые классы для ORM-системы:
- `Field` - Базовый класс для описания полей сущностей
- Специализированные поля (`IntegerField`, `StringField`, и др.)
- `CustomField` - Базовый класс для пользовательских полей
- `EntityManager` - Менеджер для выполнения операций над сущностями
- `RelatedManager` - Менеджер для работы со связанными сущностями
- `BaseEntity` - Базовый класс для всех сущностей

### entity/company.py
Определяет класс `Company` для работы с компаниями в Bitrix24.

### entity/contact.py
Определяет класс `Contact` для работы с контактами в Bitrix24.

### entity/deal.py
Определяет классы для работы со сделками:
- `Deal` - Основной класс для работы со сделками (экспортируется как `_Deal`)
- `DealNote` - Класс для работы с примечаниями к сделкам
- `Product` - Класс для работы с товарами сделки
- `ProductsManager` - Менеджер для работы с товарными позициями сделки
- Интеграция с `ActivityManager` для работы с делами CRM

### entity/note.py
Определяет класс `Note` для работы с примечаниями.

### entity/activity.py
Определяет классы для работы с делами CRM:
- `Activity` - Базовый класс для работы с активностями (звонки, встречи, email)
- `EmailActivity` - Специализированный класс для email-активностей
- `ActivityManager` - Менеджер для работы с активностями сущности
- `ActivityEntityManager` - Менеджер для операций с активностями

### entity/timeline.py
Определяет классы для работы с таймлайном CRM:
- `TimelineComment` - Класс для работы с комментариями таймлайна
- `TimelineCommentManager` - Менеджер для работы с комментариями таймлайна
- `TimelineManager` - Менеджер для работы с таймлайном сущности
- `TimelineCommentEntityManager` - Менеджер для операций с комментариями таймлайна

### entity/portal.py
Определяет классы для работы с порталом Bitrix24 и управления полями сущностей:
- `FieldInfo` - Класс для представления информации о поле сущности с метаданными
- `FieldsManager` - Базовый менеджер для работы с полями любой сущности
- `DealFieldsManager` - Специализированный менеджер полей для сделок
- `ContactFieldsManager` - Специализированный менеджер полей для контактов
- `CompanyFieldsManager` - Специализированный менеджер полей для компаний
- `LeadFieldsManager` - Специализированный менеджер полей для лидов
- `EntityFieldsContainer` - Контейнер для группировки менеджеров полей
- `Portal` - Главный класс для доступа к управлению полями всех сущностей

### entity/deal.pyi
Stub-файл для IDE с аннотациями типов для автодополнения, включая:
- Типы всех полей, включая пользовательские
- Типы для связанных объектов (company, contact)
- Возвращаемые типы для методов

### tests/conftest.py
Конфигурация для pytest:
- Загрузка переменных окружения
- Проверка наличия необходимых переменных перед запуском тестов

### tests/test_deal.py
Тесты для проверки работы с сущностью "Сделка":
- Создание сделки (test_deal_create)
- Получение сделки по ID (test_deal_get)
- Обновление полей сделки (test_deal_update)
- Фильтрация сделок (test_deal_filter)
- Удаление сделки (test_deal_delete)
- Работа с пользовательскими полями (test_custom_fields)

### portal_example.py
Пример использования Portal для работы с полями сущностей:
- Получение всех полей различных сущностей
- Создание и удаление пользовательских полей
- Фильтрация пользовательских полей
- Работа с метаданными полей
- Демонстрация API для всех поддерживаемых сущностей

## Принцип работы

1. Данные из API Bitrix24 преобразуются в объекты соответствующих классов
2. Доступ к полям и изменение полей осуществляется через соответствующие свойства объектов
3. Связанные объекты загружаются при обращении к ним (lazy loading)
4. Для сохранения изменений используется метод `save()`
5. Для выборки по фильтру используется метод `filter(**kwargs)`
6. Для получения всех сущностей используется метод `get_all()`
7. Для получения сущности по ID используется метод `get_by_id(id)`
8. Для удаления сущности используется метод `delete()`
9. Пользовательские поля добавляются через наследование от базового класса `_Deal`
10. Товары сделки управляются через объект `deal.products`
11. Дела CRM (активности) управляются через объект `deal.activity` и `lead.activity`
12. Таймлайн сущности доступен через объект `deal.timeline`, `lead.timeline`, и т.д.
13. Управление полями сущностей осуществляется через класс `Portal` с доступом к полям всех сущностей
14. Создание и удаление пользовательских полей для любых сущностей через методы `create()` и `delete()`
15. Получение полной информации о полях (включая метаданные) через `get_all()` и `get_by_name()`

## Управление полями через Portal

Новый функционал для работы с полями сущностей Bitrix24 обеспечивается через класс `Portal`. Этот класс предоставляет унифицированный интерфейс для:

### Основные возможности Portal:
- **Получение полей**: `portal.deal.fields.get_all()` - возвращает все поля сущности включая пользовательские
- **Создание полей**: `portal.deal.fields.create()` - создание новых пользовательских полей
- **Удаление полей**: `portal.deal.fields.delete()` - удаление пользовательских полей  
- **Поиск полей**: `portal.deal.fields.get_by_name()` - получение информации о конкретном поле
- **Фильтрация**: `portal.deal.fields.get_custom_fields()` - получение только пользовательских полей

### Поддерживаемые сущности:
- `portal.deal.fields` - поля сделок
- `portal.contact.fields` - поля контактов
- `portal.company.fields` - поля компаний
- `portal.lead.fields` - поля лидов

### Возможности FieldInfo:
Каждое поле представлено объектом `FieldInfo` с метаданными:
- `name` - имя поля в Bitrix24
- `title` - отображаемое название
- `type` - тип поля (string, integer, boolean и др.)
- `is_required` - обязательность поля
- `is_custom` - является ли поле пользовательским
- `settings` - дополнительные настройки поля

## Пользовательские поля

Пользовательские поля в Bitrix24 (с префиксом UF_) поддерживаются через:

1. Базовый класс `CustomField` и его специализации:
   - `TextCustomField` - для текстовых полей
   - `SelectCustomField` - для полей выбора
   - `UrlCustomField` - для URL полей

2. Добавление полей через наследование:
   ```python
   from entity import _Deal, CustomField, TextCustomField
   
   # Расширяем базовый класс _Deal, добавляя пользовательские поля
   class Deal(_Deal):
       utm_source = CustomField("UTM_SOURCE")
       delivery_address = TextCustomField("UF_CRM_DELIVERY_ADDRESS")
   ```

3. Особенности именования:
   - Если передаётся точное имя поля в Bitrix24 (начинающееся с UF_), оно используется как есть
   - В противном случае система автоматически добавляет префикс UF_ и переводит имя в верхний регистр

4. Поддержка автодополнения в IDE через stub-файлы (.pyi)

## Тестирование

### Запуск тестов

Для запуска тестов используется pytest:

```bash
pytest -xvs tests/
```

### Требования для тестов

1. Установить зависимости для тестов:
   ```bash
   pip install pytest pytest-asyncio
   ```

2. Настроить переменные окружения:
   - `WEBHOOK` - URL вебхука для доступа к API Bitrix24

### Структура тестов

Тесты построены с использованием pytest и pytest-asyncio для асинхронного тестирования.
Используются фикстуры для:
- Инициализации клиента Bitrix24
- Создания тестовых сущностей перед тестами
- Очистки тестовых данных после тестов

## Примеры использования

```python
# Определение пользовательских полей через наследование
from entity import _Deal, CustomField, TextCustomField 

class Deal(_Deal):
    utm_source = CustomField("UTM_SOURCE")
    delivery_address = TextCustomField("UF_CRM_DELIVERY_ADDRESS")

# Инициализация
bitrix = Bitrix(webhook_url)
Deal.get_manager(bitrix)
Company.get_manager(bitrix)  # Инициализация для связанных сущностей

# Получение всех сделок
deals = await Deal.objects.get_all()

# Доступ к полям
print(deal.title)

# Доступ к связанному объекту (проверка если корутина)
company_result = deal.company
if inspect.iscoroutine(company_result):
    company = await company_result
else:
    company = company_result
    
# Изменение полей
deal.title = "Новое название"
await deal.save()

# Работа с пользовательскими полями
deal.utm_source = "google"
deal.delivery_address = "ул. Примерная, д.1"
await deal.save()

# Добавление примечания
await deal.notes.create(text="Примечание")

# Работа с товарами сделки
product = deal.products.add(product_id=123, price=1000)
await deal.save()

# Получение сделки по ID
deal = await Deal.objects.get_by_id(123)

# Удаление сделки
success = await deal.delete()
if success:
    print("Сделка успешно удалена")

# Фильтрация
deals = await Deal.objects.filter(stage_id="NEW")

# Работа с активностями (делами CRM)
# Создание email-активности для контакта сделки
email_activity = await deal.activity.mail(
    subject="Коммерческое предложение",
    message="Добрый день! Высылаем коммерческое предложение...",
    contact_id=deal.contact_id  # Отправка контакту из сделки
)

# Создание email-активности на произвольный email
email_activity = await deal.activity.mail(
    subject="Коммерческое предложение", 
    message="Добрый день! Высылаем коммерческое предложение...",
    to_email="client@example.com"  # Отправка на внешний email
)

# Создание звонка
call_activity = await deal.activity.create_call(
    subject="Обзвон клиента",
    phone="+7999123456",
    description="Обсуждение условий сделки"
)

# Создание встречи
meeting_activity = await deal.activity.create_meeting(
    subject="Деловая встреча",
    location="Офис компании",
    description="Презентация продукта"
)

# Получение всех активностей сделки
activities = await deal.activity.get_all()

# Работа с активностями для лидов
lead_email = await lead.activity.mail(
    subject="Первичный контакт",
    message="Спасибо за интерес к нашим услугам",
    to_email="potential@client.com"
)

# Работа с таймлайном
# Получение всех комментариев из таймлайна сделки
comments = await deal.timeline.comments.get_all()

# Добавление комментария в таймлайн сделки
comment = await deal.timeline.comments.create(
    comment="Важная информация по сделке"
)



# Работа с таймлайном лида
lead_comment = await lead.timeline.comments.create(
    comment="Клиент запросил дополнительную информацию"
)

# Работа с полями сущностей через Portal
from entity import Portal

# Инициализация Portal
portal = Portal(bitrix)

# Получение всех полей сделки (включая пользовательские)
deal_fields = await portal.deal.fields.get_all()
print(f"Всего полей сделки: {len(deal_fields)}")

# Получение только пользовательских полей
custom_fields = await portal.deal.fields.get_custom_fields()
for field in custom_fields:
    print(f"Пользовательское поле: {field.name} - {field.title}")

# Создание нового пользовательского поля для сделки
new_field = await portal.deal.fields.create(
    field_name="utm_source",
    field_title="Источник UTM",
    field_type="string",
    is_required=False
)

# Создание поля выбора с вариантами
choice_field = await portal.deal.fields.create(
    field_name="delivery_type",
    field_title="Тип доставки",
    field_type="enumeration",
    settings={
        'DISPLAY': 'LIST',
        'LIST_HEIGHT': 3
    }
)

# Получение информации о конкретном поле
field_info = await portal.deal.fields.get_by_name("UF_UTM_SOURCE")
if field_info:
    print(f"Поле {field_info.name}: {field_info.title}")
    print(f"Тип: {field_info.type}, Обязательное: {field_info.is_required}")

# Работа с полями контактов
contact_fields = await portal.contact.fields.get_all()
await portal.contact.fields.create(
    field_name="telegram",
    field_title="Telegram",
    field_type="string"
)

# Работа с полями компаний
company_fields = await portal.company.fields.get_all()
await portal.company.fields.create(
    field_name="company_size",
    field_title="Размер компании",
    field_type="integer"
)

# Удаление пользовательского поля
deleted = await portal.deal.fields.delete("UF_UTM_SOURCE")
if deleted:
    print("Поле удалено")

# Получение полей всех сущностей одним запросом
all_fields = await portal.get_all_entities_fields()
for entity_name, fields in all_fields.items():
    print(f"{entity_name}: {len(fields)} полей")
``` 