import asyncio
import os
from fast_bitrix24 import Bitrix
from dotenv import load_dotenv
load_dotenv()

async def test_userfield():
    webhook = os.getenv('WEBHOOK')
    if not webhook:
        print('No webhook')
        return
    
    bitrix = Bitrix(webhook)
    
    # Попробуем посмотреть список существующих пользовательских полей
    try:
        result = await bitrix.get_all('crm.userfield.list', {'filter': {'ENTITY_ID': 'CRM_DEAL'}})
        print(f'Existing userfields: {len(result)}')
        for field in result[:3]:
            print(f'  {field.get("FIELD_NAME", "Unknown")}: {field.get("EDIT_FORM_LABEL", "No label")}')
    except Exception as e:
        print(f'Error getting userfields: {e}')

asyncio.run(test_userfield()) 