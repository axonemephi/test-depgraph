from . import models
from ..util.helpers import to_title


def format_user(user: models.User) -> str:
    return f"{user.id}:{to_title(user.name)}"


def order_total(order: models.Order) -> float:
    return round(order.total, 2)



