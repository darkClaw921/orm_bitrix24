v0.1.2
- Добавлена поддержка активностей (только email)

v0.1.3
- Добавлена поддержка таймлайна (комментарии) 
    - Возможность получать и создавать комментарии у основных и связанных сущностях 

v0.1.4
- Добавлена поддержка полей сделки, контакта, компании
    - Возможность получать и создавать поля сделки, контакта, компании
        - пока можно создавать только стандартные поля (string, int)
        - получать и работать можно с полями (string, int, enumeration)
        - получать можно как все поля, так и конкретное поле по имени (get_by_name("UF_CRM_TEST_FIELD") и get_all())
    - Возможность удалять поля сделки, контакта, компании
  