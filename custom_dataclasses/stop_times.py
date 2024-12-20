from src.fields.String_ import String
from src.fields.Integer_ import Integer
from src.dataRepr import DataRepr


class StopTimes(metaclass=DataRepr):
    trip_id:String
    stop_id:String
    stop_sequence:Integer
    arrival_time:String
    departure_time:String
    pickup_type:Integer
    drop_off_type:Integer
    shape_dist_traveled:String
    stop_headsign:String
