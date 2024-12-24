
class Field:
    def set_field_name(self, field_name:str) -> None:
        self.field_name:str = field_name
    
    @property
    def python_type(self):
        raise NotImplementedError