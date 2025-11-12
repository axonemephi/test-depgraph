from . import services, models


def describe_user(user_id: int, name: str) -> str:
    user = models.User(id=user_id, name=name)
    return services.format_user(user)



