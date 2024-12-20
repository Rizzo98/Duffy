from src.fields.Field_ import Field

class DataRepr(type):
    def __new__(cls, name, bases, dct):
        if '__repr__' not in dct:
            def __repr__(self):
                return f"{name}: {', '.join([f'{k}={v}' for k,v in self.__dict__.items()])}"
            dct['__repr__'] = __repr__
        return super().__new__(cls, name, bases, dct)
    
    def __init__(cls, name, bases, namespace, **kwargs):
        for attr_name, attr_type in cls.__annotations__.items():
            if issubclass(attr_type, Field):
                    attr:Field = getattr(cls, attr_name, None)
                    attr.set_field_name(attr_name)
                    setattr(cls, attr_name, attr)
        super().__init__(name, bases, namespace, **kwargs)
    
    def __getattr__(cls, name):
        if name in cls.__annotations__:
            return cls.__annotations__[name]()