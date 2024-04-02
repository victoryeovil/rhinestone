def chunk(array: list, chunk_size: int):
    for i in range(0, len(array), chunk_size):
        yield array[i:i + chunk_size]