
class SlottedClass(type):
    def __new__(cls, name, bases, field_types):
        dct = {}
        dct['__annotations__'] = field_types
        dct['__slots__'] = tuple(dct['__annotations__'].keys())
        
        def __repr__(self):
            return f"{name}: {', '.join([f'{c}={getattr(self, c)}' for c in self.__slots__])}"
        dct['__repr__'] = __repr__

        return super().__new__(cls, name, bases, dct)