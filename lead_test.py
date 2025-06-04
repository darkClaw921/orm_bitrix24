from orm_bitrix24.entity import _Lead, CustomField, TextCustomField, SelectCustomField, Company
import asyncio
import os
from fast_bitrix24 import Bitrix
from dotenv import load_dotenv
load_dotenv()


class Lead(_Lead):
    utm_source = CustomField("UTM_SOURCE")
    delivery_address = TextCustomField("UF_CRM_DELIVERY_ADDRESS")
    delivery_type223 = SelectCustomField("UF_CRM_DELIVERY_TYPE")


async def main():
    # Инициализация клиента Bitrix24
    webhook = os.environ.get("WEBHOOK")
    if not webhook:
        print("Необходимо установить переменную окружения WEBHOOK")
        return
    
    bitrix = Bitrix(webhook)
    
    # Инициализация менеджеров сущностей
    Lead.get_manager(bitrix)
    # Company.get_manager(bitrix)

    leads = await Lead.objects.get_all()
    print(f"Найдено лидов: {len(leads)}")
    lead = leads[0]

    deal=await lead.move_to_deal()
    print(deal)
    # company=Company(bitrix)

    # company.title = "Тестовая компания2222"
    # companyID=await company.save()
    # print(companyID)
    # lead.company_id = companyID
    # await lead.save()
    
    # for lead in leads:
    #     await lead.company
    #     if lead.company:
    #         print(lead.company.title)
    #     else:
    #         print("Компания не найдена")

if __name__ == "__main__":
    asyncio.run(main())