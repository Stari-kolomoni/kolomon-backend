
def paging_filter_sort(query, params):
    limit = params.get('limit')
    skip = params.get('skip')
    if skip:
        query = query.offset(skip)
    if limit:
        query = query.limit(limit)

    return query
