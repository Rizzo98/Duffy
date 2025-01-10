from __future__ import annotations
from typing import Any, Dict, Iterator, List, Tuple, Self, Union, Type, TYPE_CHECKING
from custom_dataclasses.persona import Persona
from src.fields.Field_ import Field
from src.fields.String_ import String
from src.dataRepr import DataRepr
from src.slottedClass import SlottedClass
from functools import reduce
import duckdb
import os
import copy


if TYPE_CHECKING:
    from src.groupedCollection import GroupedCollection


class Collection:
    def __init__(self, csv_file_path:List[str], dataRepr:DataRepr):
        self.__path = os.path.join(os.getcwd(), *csv_file_path)
        assert os.path.exists(self.__path), f"File {self.__path} does not exist"
        self.__from:str = f"FROM '{self.__path}'"
        self.__select:str = '*'
        self.__select_unionChar:str = ', '
        self.__where:str = ''
        self.__limit:str = ''
        self.__dataRepr:DataRepr = dataRepr
    
    @property
    def selected_columns(self)->List[str]:
        if self.__select == '*':
            return list(self.__dataRepr.__annotations__.keys())
        else:
            return self.__select.split(self.__select_unionChar)

    def copy(self)->Self:
        return copy.deepcopy(self)

    def select(self, *columns:Union[str,Tuple[str]])->Self:
        if isinstance(columns, Field):
            columns = [columns]
        
        columns = [str(column) for column in columns]
        new_collection:Self = self.copy()
        new_collection.__select = self.__select_unionChar.join(columns)
        return new_collection
    
    def where(self, condition:String)->Self:
        new_collection:Self = self.copy()
        new_collection.__where = f'WHERE {condition.value}'
        return new_collection

    def limit(self, limit:int)->Self:
        new_collection:Self = self.copy()
        new_collection.__limit = f"LIMIT {limit}"
        return new_collection
    
    def __execute_query(self, distinct:bool=False)->duckdb.DuckDBPyRelation:
        distinct:str = 'DISTINCT' if distinct else ''
        query:str = f"""SELECT {distinct} {self.__select} {self.__from} 
            {self.__where}
            {self.__limit}
        """
        return duckdb.query(query)
    
    def collect(self)->List[DataRepr]:
        '''
        Returns a list of dataRepr objects.
        '''
        to_return:List[DataRepr] = []
        result = self.__execute_query().fetchall()
        cols:Dict[str,Type] = {col:getattr(self.__dataRepr, col).python_type for col in self.selected_columns}
        new_dataRepr:Type =  SlottedClass(self.__dataRepr.__name__, (object,), cols)

        for row in result:
            instance:SlottedClass = new_dataRepr()
            for attr_name, attr_val in zip(self.selected_columns, row):
                instance.__setattr__(attr_name, attr_val)
            to_return.append(instance)

        return to_return
     
    def iterate_over_columns(self, *columns:Tuple[String]) -> Iterator[Tuple[Any,Self]]:
        '''
        This method allows to iterate over unique values of a column.

        :Example: for value, collection in c.iterate_over_column('Age'):
            print(value) # prints the unique value of the column
            print(collection.collect()) # prints the collection of dataRepr objects that have the value in the column
        '''
        new_collection:Self = self.select(*columns)
        unique_values:List[Tuple[Any]] = new_collection.__execute_query(distinct=True).fetchall()
        for values in unique_values:
            where_conds:List[String] = []
            for i, value in enumerate(values):
                column_type:Type = type(getattr(self.__dataRepr, str(columns[i])))
                column_instance:Field = column_type(str(columns[i]))
                column_instance.set_field_name(str(columns[i]))
                where_conds.append(column_instance == value)
            
            where_cond:String = reduce(lambda c1,c2: c1&c2, where_conds)
            yield values, self.where(where_cond)
    
    def group_by(self, *columns:Tuple[String])->GroupedCollection:
        from src.groupedCollection import GroupedCollection
        return GroupedCollection(self.__from, self.__dataRepr, *columns)
    
    def count(self, *columns:Tuple[String])->int:
        '''
        Counts the number of rows in the collection.
        If columns are specified, it counts the number of rows grouped by the columns.
        '''
        if columns:
            return self.group_by(*columns).count()
        else:
            new_collection:Self = self.copy()
            new_collection.__select = 'COUNT(*)'
            return new_collection.__execute_query().fetchall()[0][0]


if __name__ == '__main__':
    c = Collection(["data", "classe.csv"], Persona)
    
    print(c.count(Persona.Gender))

    for t,v in c.group_by(Persona.Gender).count().items():
        print(t, v)

    for t,v in c.group_by(Persona.Gender).sum(Persona.Age, Persona.Salary).items():
        print(t, v)

    for value, collection in c.iterate_over_columns(Persona.Gender):
        persone = collection.collect()
        print(value)
        print(persone)

    l = c.select(Persona.Age, Persona.Gender)\
        .where((Persona.Age > 40) | (Persona.Gender == 'Female'))\
        .collect()
    
    print(l)