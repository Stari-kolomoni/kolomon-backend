from sqlalchemy.orm import Session


def paging_filter_sort(query, params):
    if skip := params.get('skip'):
        query = query.offset(skip)
    if limit := params.get('limit'):
        query = query.limit(limit)

    return query

