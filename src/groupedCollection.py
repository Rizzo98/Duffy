from typing import Any, Dict, List, Optional, Tuple, Type, Union
from src.fields.String_ import String
from src.dataRepr import DataRepr
from src.slottedClass import SlottedClass
import duckdb


class GroupedCollection:
    AGGREGATORS:List[str] = ('count', 'sum')
    AGGREGATOR_ARG_CONNECTOR:str = '_'

    def __init__(self, from_:str, dataRepr:DataRepr, *group_by:Tuple[String]):
        self.__select:str = ', '.join([str(column) for column in group_by])
        self.__select_unionChar:str = ', '
        self.__from:str = from_
        self.__dataRepr:DataRepr = dataRepr
        self.__aggregate_select:str = ''
        self.__group_by_columns_str:str = f" GROUP BY {', '.join([str(column) for column in group_by])}"
    
    @property
    def selected_columns(self)->List[str]:
        if self.__select == '*':
            return list(self.__dataRepr.__annotations__.keys())
        else:
            return self.__select.split(self.__select_unionChar)
    
    def __execute_query(self)->duckdb.DuckDBPyRelation:
        query:str = f"""SELECT {self.__select} {self.__aggregate_select}
            {self.__from}
            {self.__group_by_columns_str}
        """
        return duckdb.query(query)
    
    def __add_aggregation(self, *aggregations:Tuple[str], args:Union[str,Tuple[str]]=('',))->None:
        for aggregation in aggregations:
            for arg in args:
                if aggregation == GroupedCollection.AGGREGATORS[0]:
                    self.__aggregate_select += f", COUNT({arg}) AS {GroupedCollection.AGGREGATORS[0]}{GroupedCollection.AGGREGATOR_ARG_CONNECTOR}{arg}"
                elif aggregation == GroupedCollection.AGGREGATORS[1]:
                    self.__aggregate_select += f", SUM({arg}) AS {GroupedCollection.AGGREGATORS[1]}{GroupedCollection.AGGREGATOR_ARG_CONNECTOR}{arg}"

    def __execute_aggregation(self, number_of_aggregations:int=1)->Dict[DataRepr, Any]:
        res = self.__execute_query()
        columns:List[str] = res.columns
        result:List[Tuple[Any]] = res.fetchall()
        
        cols:Dict[str,Type] = {col:getattr(self.__dataRepr, col).python_type for col in self.selected_columns}
        new_dataRepr:Type =  SlottedClass(self.__dataRepr.__name__, (object,), cols)
        to_return:Dict[DataRepr, int] = {}
        for row in result:
            instance:DataRepr = new_dataRepr()
            values:Any = 0
            if number_of_aggregations>1:
                values = {}
            for col_arg,v in zip(columns, row):
                col_arg_split:List[str] = col_arg.split(f'{GroupedCollection.AGGREGATOR_ARG_CONNECTOR}')
                column = col_arg_split[0]
                arg:Optional[str] = None if len(col_arg_split)==1 else col_arg_split[1]
                if not column in GroupedCollection.AGGREGATORS:
                    instance.__setattr__(column, v)
                else:
                    if number_of_aggregations==1:
                        values = v
                    else:
                        values[arg] = v
            to_return[instance] = values
        return to_return

    def count(self)->Dict[DataRepr, int]:
        self.__add_aggregation(GroupedCollection.AGGREGATORS[0])
        return self.__execute_aggregation()
    
    def sum(self, *columns:Tuple[String])->Dict[DataRepr, int]:
        self.__add_aggregation(GroupedCollection.AGGREGATORS[1], args=columns)
        return self.__execute_aggregation(number_of_aggregations=len(columns))