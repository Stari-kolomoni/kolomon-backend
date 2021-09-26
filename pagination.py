class Pagination:
    skip: int
    limit: int

    def __init__(self, skip, limit):
        self.skip = skip
        self.limit = limit


class Paginator:

    data_size: int

    def __init__(self, data_size):
        self.data_size = data_size

    def paginate(self, page: int):
        skip = self.data_size * page
        return Pagination(skip, self.data_size)
