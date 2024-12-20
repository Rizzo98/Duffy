from .Field_ import Field
from typing import Self


class String(Field):
    __slots__ = ("_value",)

    def __init__(self, value:str=""):
        self._value = value

    @property
    def value(self):
        return self._value

    def __repr__(self):
        return self.field_name

    def __eq__(self, value) -> Self:
        return String(f"{self.field_name} LIKE '{value}'")
        
    def __ne__(self, value) -> Self:
        return String(f"{self.field_name} != '{value}'")
    
    def __and__(self, other:Self) -> Self:
        return String(f"{self.value} AND {other.value}")
    
    def __or__(self, other:Self) -> Self:
        return String(f"{self.value} OR {other.value}")