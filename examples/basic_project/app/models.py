from dataclasses import dataclass


@dataclass
class User:
    id: int
    name: str


@dataclass
class Order:
    id: int
    user_id: int
    total: float



