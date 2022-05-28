from sqlalchemy.sql import Select
from starlette.datastructures import QueryParams


# noinspection PyNoneFunctionAssignment
def paging_filter_sort(query: Select, params: QueryParams) -> Select:
    """
    Parse the QueryParams dictionary and apply pagination accordingly.

    :param query: Select statement to paginate.
    :param params: Pagination parameters.
        Expected: "skip" integer to specify the offset, "limit" to specify the amount to return.
    :return:
    """
    if skip := params.get("skip"):
        query = query.offset(skip)
    if limit := params.get("limit"):
        query = query.limit(limit)

    return query
