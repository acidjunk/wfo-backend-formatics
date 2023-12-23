users = [
    {"user_id": "4af1f7f5-4781-4607-bf6c-f0388f7f4527", "first_name": "Rene", "is_paying_user": True, "user_email_address": "acidjunk@gmail.com"},
    {"user_id": "4f7b3111-2740-44b1-b2dd-b2c5a4e6af54", "first_name": "René", "is_paying_user": False,"user_email_address": "rene@formatics.nl"},
]


class CrmException(Exception):
    pass


def get_users():
    # Todo: add form to select company
    return users


def get_user_by_id(user_id):
    for user in users:
        if user["user_id"] == user_id:
            return user
    raise CrmException(f"Couldn't resolve user_id: {user_id}")
