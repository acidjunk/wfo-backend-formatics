companies = [
    {"user_id": "4af1f7f5-4781-4607-bf6c-f0388f7f4527", "first_name": "Rene", "is_paying_user": True, "user_email_address": "acidjunk@gmail.com"},
    {"user_id": "4f7b3111-2740-44b1-b2dd-b2c5a4e6af54", "first_name": "René", "is_paying_user": False,"user_email_address": "rene@formatics.nl"},
]


class CrmException(Exception):
    pass


def get_companies():
    # Todo: add form to select company
    return companies


def get_company_by_id(company_id):
    for company in companies:
        if company["company_id"] == company_id:
            return company
    raise CrmException(f"Couldn't resolve company_id: {company_id}")
