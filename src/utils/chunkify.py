from itertools import islice
from src.dataRepr import DataRepr

#TODO: da implementare in collect
def chunkify(iterable, chunk_size):
    """
    Yields chunks of the given size from an iterable.
    """
    iterable = iter(iterable)
    while chunk := list(islice(iterable, chunk_size)):
        yield chunk

def process_chunk(chunk, data_repr_name, selected_columns):
    # Dynamically fetch the DataRepr class using its name
    new_dataRepr = getattr(DataRepr, data_repr_name)
    processed = []
    for row in chunk:
        instance = new_dataRepr()
        for attr_name, attr_val in zip(selected_columns, row):
            instance.__setattr__(attr_name, attr_val)
        processed.append(instance)
    return processed