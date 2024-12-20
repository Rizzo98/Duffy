from src.fields.String_ import String
from src.fields.Integer_ import Integer
from src.dataRepr import DataRepr


class Persona(metaclass=DataRepr):
    Name:String
    Surname: String
    Gender: String
    Age: Integer
    Salary: Integer


if __name__ == '__main__':
    print(Persona.Age > 25)
    print(Persona.Name == "John")
    print((Persona.Name == "John") & (Persona.Age > 25))