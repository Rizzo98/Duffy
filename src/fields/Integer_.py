from .Field_ import Field
from .String_ import String


class Integer(Field):
    __slots__ = ("_value",)

    def __init__(self, value:int=0):
        self._value = value

    @property
    def value(self):
        return self._value

    @property
    def python_type(self):
        return int
    
    def __repr__(self):
        return self.field_name
       
    def __eq__(self, value:int)->str:
        return String(f'{self.field_name} = {value}')
    
    def __ne__(self, value:int)->str:
        return String(f'{self.field_name} != {value}')

    def __lt__(self, value:int)->str:
        return String(f'{self.field_name} < {value}')
    
    def __le__(self, value:int)->str:
        return String(f'{self.field_name} <= {value}')
    
    def __gt__(self, value:int)->str:
        return String(f'{self.field_name} > {value}')
    
    def __ge__(self, value:int)->str:
        return String(f'{self.field_name} >= {value}')